# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
import time
import warnings
import unified_planning as up
import pytamer # type: ignore
import unified_planning.plans
import unified_planning.engines
import unified_planning.engines.mixins
from unified_planning.model import ProblemKind
from unified_planning.engines import PlanGenerationResultStatus, ValidationResult, ValidationResultStatus, Credits
from up_tamer.converter import Converter
from fractions import Fraction
from ConfigSpace import ConfigurationSpace
from typing import IO, Callable, Optional, Dict, List, Tuple, Union, Set, cast


credits = Credits('Tamer',
                  'FBK Tamer Development Team',
                  'tamer@fbk.eu',
                  'https://tamer.fbk.eu',
                  'Free for Educational Use',
                  'Tamer offers the capability to generate a plan for classical, numerical and temporal problems.\nFor those kind of problems tamer also offers the possibility of validating a submitted plan.',
                  'Tamer offers the capability to generate a plan for classical, numerical and temporal problems.\nFor those kind of problems tamer also offers the possibility of validating a submitted plan.\nYou can find all the related publications here: https://tamer.fbk.eu/publications/'
                )

class TState(up.model.State):
    def __init__(self, ts: pytamer.tamer_state,
                 interpretation: pytamer.tamer_interpretation,
                 converter: Converter,
                 problem: 'up.model.Problem',
                 static_fluents: Set["up.model.fluent.Fluent"]):
        self._ts = ts
        self._interpretation = interpretation
        self._converter = converter
        self._problem = problem
        self._static_fluents = static_fluents

    def get_value(self, f: 'up.model.FNode') -> 'up.model.FNode':
        if f.fluent() in self._static_fluents:
            return self._problem.initial_value(f)
        cf = self._converter.convert(f)
        r = pytamer.tamer_state_get_value(self._ts, self._interpretation, cf)
        cr = self._converter.convert_back(r)
        return cr


class EngineImpl(
        up.engines.Engine,
        up.engines.mixins.OneshotPlannerMixin,
        up.engines.mixins.PlanValidatorMixin
    ):
    """ Implementation of the up-tamer Engine. """

    def __init__(self, weight: Optional[float] = None,
                 heuristic: Optional[str] = None, **options):
        up.engines.Engine.__init__(self)
        up.engines.mixins.OneshotPlannerMixin.__init__(self)
        up.engines.mixins.PlanValidatorMixin.__init__(self)
        self._env = pytamer.tamer_env_new()
        if not weight is None:
            pytamer.tamer_env_set_float_option(self._env, 'weight', weight)
        self._heuristic = heuristic
        if len(options) > 0:
            raise up.exceptions.UPUsageError('Custom options not supported!')
        self._bool_type = pytamer.tamer_boolean_type(self._env)
        self._tamer_start = \
            pytamer.tamer_expr_make_point_interval(self._env,
                                                   pytamer.tamer_expr_make_start_anchor(self._env))
        self._tamer_end = \
            pytamer.tamer_expr_make_point_interval(self._env,
                                                   pytamer.tamer_expr_make_end_anchor(self._env))

    @property
    def name(self) -> str:
        return 'Tamer'

    @staticmethod
    def supported_kind() -> ProblemKind:
        supported_kind = ProblemKind(version=2)
        supported_kind.set_problem_class('ACTION_BASED')
        supported_kind.set_time('CONTINUOUS_TIME')
        supported_kind.set_time('INTERMEDIATE_CONDITIONS_AND_EFFECTS')
        supported_kind.set_time('TIMED_EFFECTS')
        supported_kind.set_time('TIMED_GOALS')
        supported_kind.set_time('DURATION_INEQUALITIES')
        supported_kind.set_expression_duration('STATIC_FLUENTS_IN_DURATIONS')
        supported_kind.set_expression_duration('FLUENTS_IN_DURATIONS')
        supported_kind.set_expression_duration("INT_TYPE_DURATIONS")
        supported_kind.set_expression_duration("REAL_TYPE_DURATIONS")
        supported_kind.set_numbers("BOUNDED_TYPES")
        supported_kind.set_problem_type("SIMPLE_NUMERIC_PLANNING")
        supported_kind.set_problem_type("GENERAL_NUMERIC_PLANNING")
        supported_kind.set_typing('FLAT_TYPING')
        supported_kind.set_parameters("BOOL_FLUENT_PARAMETERS")
        supported_kind.set_parameters("BOUNDED_INT_FLUENT_PARAMETERS")
        supported_kind.set_parameters("BOOL_ACTION_PARAMETERS")
        supported_kind.set_parameters("BOUNDED_INT_ACTION_PARAMETERS")
        supported_kind.set_effects_kind('INCREASE_EFFECTS')
        supported_kind.set_effects_kind('DECREASE_EFFECTS')
        supported_kind.set_effects_kind("STATIC_FLUENTS_IN_BOOLEAN_ASSIGNMENTS")
        supported_kind.set_effects_kind("STATIC_FLUENTS_IN_NUMERIC_ASSIGNMENTS")
        supported_kind.set_effects_kind("STATIC_FLUENTS_IN_OBJECT_ASSIGNMENTS")
        supported_kind.set_effects_kind("FLUENTS_IN_BOOLEAN_ASSIGNMENTS")
        supported_kind.set_effects_kind("FLUENTS_IN_NUMERIC_ASSIGNMENTS")
        supported_kind.set_effects_kind("FLUENTS_IN_OBJECT_ASSIGNMENTS")
        supported_kind.set_conditions_kind('NEGATIVE_CONDITIONS')
        supported_kind.set_conditions_kind('DISJUNCTIVE_CONDITIONS')
        supported_kind.set_conditions_kind('EQUALITIES')
        supported_kind.set_fluents_type("INT_FLUENTS")
        supported_kind.set_fluents_type("REAL_FLUENTS")
        supported_kind.set_fluents_type('OBJECT_FLUENTS')
        supported_kind.set_simulated_entities('SIMULATED_EFFECTS')
        return supported_kind

    @staticmethod
    def supports(problem_kind: 'up.model.ProblemKind') -> bool:
        return problem_kind <= EngineImpl.supported_kind()

    @staticmethod
    def supports_plan(plan_kind: 'up.plans.PlanKind') -> bool:
        return plan_kind in [up.plans.PlanKind.SEQUENTIAL_PLAN, up.plans.PlanKind.TIME_TRIGGERED_PLAN]

    @staticmethod
    def satisfies(optimality_guarantee: up.engines.OptimalityGuarantee) -> bool:
        return False

    @staticmethod
    def get_credits(**kwargs) -> Optional[up.engines.Credits]:
        return credits

    @staticmethod
    def get_configuration_space() -> ConfigurationSpace:
        return ConfigurationSpace(space={"weight": (0.0, 1.0), "heuristic": ["hadd", "hlandmarks", "hmax", "hff", "blind"]})

    def _validate(self, problem: 'up.model.AbstractProblem', plan: 'up.plans.Plan') -> 'up.engines.results.ValidationResult':
        assert isinstance(problem, up.model.Problem)
        tproblem, _ = self._convert_problem(problem)
        tplan = self._convert_plan(tproblem, plan)
        epsilon = None
        if problem.epsilon is not None:
            epsilon = problem.epsilon
        elif plan.kind == up.plans.PlanKind.TIME_TRIGGERED_PLAN:
            epsilon = plan.extract_epsilon(problem)
        if epsilon is not None:
            pytamer.tamer_env_set_string_option(self._env, "plan-epsilon", str(epsilon))
        start = time.time()
        value = pytamer.tamer_ttplan_validate(tproblem, tplan) == 1
        solving_time = time.time() - start
        return ValidationResult(ValidationResultStatus.VALID if value else ValidationResultStatus.INVALID,
                                self.name, [], metrics={"engine_internal_time": str(solving_time)})

    def _solve(self, problem: 'up.model.AbstractProblem',
               heuristic: Optional[Callable[["up.model.state.State"], Optional[float]]] = None,
               timeout: Optional[float] = None,
               output_stream: Optional[IO[str]] = None) -> 'up.engines.results.PlanGenerationResult':
        assert isinstance(problem, up.model.Problem)
        if timeout is not None:
            warnings.warn('Tamer does not support timeout.', UserWarning)
        if output_stream is not None:
            warnings.warn('Tamer does not support output stream.', UserWarning)
        tproblem, converter = self._convert_problem(problem)
        heuristic_fun = None
        if heuristic is not None:
            static_fluents = problem.get_static_fluents()
            def fun(ts: pytamer.tamer_classical_state,
                    interpretation: pytamer.tamer_interpretation) -> float:
                s = TState(ts, interpretation, converter, problem, static_fluents)
                res = heuristic(s)
                if res is None:
                    return -1
                else:
                    return res
            heuristic_fun = fun
        if problem.kind.has_continuous_time():
            pytamer.tamer_env_set_boolean_option(self._env, "simultaneity", 1)
            pytamer.tamer_env_set_boolean_option(self._env, "ftp-deordering-plan", 1)
            if self._heuristic is not None:
                if isinstance(self._heuristic, str):
                    heuristics = [self._heuristic]
                else:
                    assert isinstance(self._heuristic, list)
                    heuristics = self._heuristic
                pytamer.tamer_env_set_vector_string_option(self._env, 'ftp-heuristic', heuristics)
            elif heuristic is not None:
                pytamer.tamer_env_set_vector_string_option(self._env, 'ftp-heuristic', [])
            else:
                pytamer.tamer_env_set_vector_string_option(self._env, 'ftp-heuristic', ['hadd'])
            if problem.epsilon is not None:
                pytamer.tamer_env_set_string_option(self._env, "plan-epsilon", str(problem.epsilon))
            else:
                pytamer.tamer_env_set_string_option(self._env, "plan-epsilon", "0.01")
            start = time.time()
            ttplan = pytamer.tamer_do_ftp_planning(tproblem, heuristic_fun)
            solving_time = time.time() - start
            if pytamer.tamer_ttplan_is_error(ttplan) == 1:
                ttplan = None
        else:
            if self._heuristic is not None:
                pytamer.tamer_env_set_string_option(self._env, 'tsimple-heuristic', self._heuristic)
            else:
                pytamer.tamer_env_set_string_option(self._env, 'tsimple-heuristic', "hadd")
            ttplan, solving_time = self._solve_classical_problem(tproblem, heuristic_fun)
        plan = self._to_up_plan(problem, ttplan)
        status = PlanGenerationResultStatus.UNSOLVABLE_INCOMPLETELY if plan is None else PlanGenerationResultStatus.SOLVED_SATISFICING
        return up.engines.PlanGenerationResult(status, plan, self.name, metrics={"engine_internal_time": str(solving_time)})

    def _convert_type(self, typename: 'up.model.Type',
                      user_types_map: Dict['up.model.Type', pytamer.tamer_type]) -> pytamer.tamer_type:
        if typename.is_bool_type():
            ttype = self._bool_type
        elif typename.is_user_type():
            ttype = user_types_map[typename]
        elif typename.is_int_type():
            typename = cast(up.model.types._IntType, typename)
            ilb = typename.lower_bound
            iub = typename.upper_bound
            if ilb is None and iub is None:
                ttype = pytamer.tamer_integer_type(self._env)
            elif ilb is None:
                ttype = pytamer.tamer_integer_type_ub(self._env, iub)
            elif iub is None:
                ttype = pytamer.tamer_integer_type_lb(self._env, ilb)
            else:
                ttype = pytamer.tamer_integer_type_lub(self._env, ilb, iub)
        elif typename.is_real_type():
            typename = cast(up.model.types._RealType, typename)
            flb = typename.lower_bound
            fub = typename.upper_bound
            if flb is None and fub is None:
                ttype = pytamer.tamer_rational_type(self._env)
            elif flb is None:
                ttype = pytamer.tamer_rational_type_ub(self._env, float(fub))
            elif fub is None:
                ttype = pytamer.tamer_rational_type_lb(self._env, float(flb))
            else:
                ttype = pytamer.tamer_rational_type_lub(self._env, float(flb), float(fub))
        else:
            raise NotImplementedError
        return ttype

    def _convert_fluent(self, fluent: 'up.model.Fluent',
                        user_types_map: Dict['up.model.Type', pytamer.tamer_type]) -> pytamer.tamer_fluent:
        typename = fluent.type
        ttype = self._convert_type(typename, user_types_map)
        params = []
        for param in fluent.signature:
            ptype = self._convert_type(param.type, user_types_map)
            p = pytamer.tamer_parameter_new(param.name, ptype)
            params.append(p)
        return pytamer.tamer_fluent_new(self._env, fluent.name, ttype, [], params)

    def _convert_constant(self, constant: 'up.model.Fluent',
                          constants_assignments: List[Tuple[List[pytamer.tamer_expr], pytamer.tamer_expr]],
                          user_types_map: Dict['up.model.Type', pytamer.tamer_type]) -> pytamer.tamer_constant:
        typename = constant.type
        ttype = self._convert_type(typename, user_types_map)
        params = []
        for param in constant.signature:
            ptype = self._convert_type(param.type, user_types_map)
            p = pytamer.tamer_parameter_new(param.name, ptype)
            params.append(p)
        values = pytamer.tamer_function_value_new()
        for key, value in constants_assignments:
            pytamer.tamer_function_value_add_assignment(values, key, value)
        return pytamer.tamer_constant_new(self._env, constant.name, ttype, [], params, values)

    def _convert_timing(self, timing: 'up.model.Timing') -> pytamer.tamer_expr:
        k = Fraction(timing.delay)
        if k < 0:
            c = pytamer.tamer_expr_make_rational_constant(self._env, -k.numerator, k.denominator)
        else:
            c = pytamer.tamer_expr_make_rational_constant(self._env, k.numerator, k.denominator)
        if timing.is_from_start():
            if k == 0:
                return self._tamer_start
            else:
                assert k > 0
                s = pytamer.tamer_expr_make_start_anchor(self._env)
                r = pytamer.tamer_expr_make_plus(self._env, s, c)
                return pytamer.tamer_expr_make_point_interval(self._env, r)
        elif timing.is_from_end():
            if k == 0:
                return self._tamer_end
            else:
                assert k < 0
                s = pytamer.tamer_expr_make_end_anchor(self._env)
                r = pytamer.tamer_expr_make_minus(self._env, s, c)
                return pytamer.tamer_expr_make_point_interval(self._env, r)
        else:
            return pytamer.tamer_expr_make_point_interval(self._env, c)

    def _convert_interval(self, interval: 'up.model.TimeInterval') -> pytamer.tamer_expr:
        if interval.lower == interval.upper:
            return self._convert_timing(interval.lower)
        lower = pytamer.tamer_expr_get_child(self._convert_timing(interval.lower), 0)
        upper = pytamer.tamer_expr_get_child(self._convert_timing(interval.upper), 0)
        if interval.is_left_open() and interval.is_right_open():
            return pytamer.tamer_expr_make_open_interval(self._env, lower, upper)
        elif interval.is_left_open():
            return pytamer.tamer_expr_make_left_open_interval(self._env, lower, upper)
        elif interval.is_right_open():
            return pytamer.tamer_expr_make_right_open_interval(self._env, lower, upper)
        else:
            return pytamer.tamer_expr_make_closed_interval(self._env, lower, upper)

    def _convert_duration(self, converter: Converter,
                          duration: 'up.model.DurationInterval') -> pytamer.tamer_expr:
        d = pytamer.tamer_expr_make_duration_anchor(self._env)
        lower = converter.convert(duration.lower)
        upper = converter.convert(duration.upper)
        if duration.lower == duration.upper:
            return pytamer.tamer_expr_make_equals(self._env, d, lower)
        if duration.is_left_open():
            l = pytamer.tamer_expr_make_gt(self._env, d, lower)
        else:
            l = pytamer.tamer_expr_make_ge(self._env, d, lower)
        if duration.is_right_open():
            u = pytamer.tamer_expr_make_lt(self._env, d, upper)
        else:
            u = pytamer.tamer_expr_make_le(self._env, d, upper)
        return pytamer.tamer_expr_make_and(self._env, l, u)

    def _convert_simulated_effect(self, converter: Converter, problem: 'up.model.Problem',
                                  action: 'up.model.Action', timing: 'up.model.Timing',
                                  sim_eff: 'up.model.SimulatedEffect') -> pytamer.tamer_simulated_effect:
        fluents = [converter.convert(x) for x in sim_eff.fluents]
        static_fluents = problem.get_static_fluents()
        def f(ts: pytamer.tamer_classical_state,
              interpretation: pytamer.tamer_interpretation,
              actual_params: pytamer.tamer_vector_expr,
              res: pytamer.tamer_vector_expr):
            s = TState(ts, interpretation, converter, problem, static_fluents)
            actual_params_dict = {}
            for i, p in enumerate(action.parameters):
                tvalue = pytamer.tamer_vector_get_expr(actual_params, i)
                actual_params_dict[p] = converter.convert_back(tvalue)
            vec = sim_eff.function(problem, s, actual_params_dict)
            for x in vec:
                pytamer.tamer_vector_add_expr(res, converter.convert(x))
        return pytamer.tamer_simulated_effect_new(self._convert_timing(timing), fluents, f);

    def _convert_action(self, problem: 'up.model.Problem', action: 'up.model.Action',
                        fluents_map: Dict['up.model.Fluent', pytamer.tamer_fluent],
                        constants_map: Dict['up.model.Fluent', pytamer.tamer_constant],
                        user_types_map: Dict['up.model.Type', pytamer.tamer_type],
                        instances_map: Dict['up.model.Object', pytamer.tamer_instance]) -> pytamer.tamer_action:
        params = []
        params_map = {}
        for p in action.parameters:
            ptype = self._convert_type(p.type, user_types_map)
            new_p = pytamer.tamer_parameter_new(p.name, ptype)
            params.append(new_p)
            params_map[p] = new_p
        expressions = []
        simulated_effects = []
        converter = Converter(self._env, problem, fluents_map, constants_map, instances_map, params_map)
        if isinstance(action, up.model.InstantaneousAction):
            for c in action.preconditions:
                expr = pytamer.tamer_expr_make_temporal_expression(self._env, self._tamer_start,
                                                                   converter.convert(c))
                expressions.append(expr)
            for e in action.effects:
                assert not e.is_conditional()
                if e.is_assignment():
                    ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(e.fluent), converter.convert(e.value))
                elif e.is_increase():
                    val = pytamer.tamer_expr_make_plus(self._env, converter.convert(e.fluent), converter.convert(e.value))
                    ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(e.fluent), val)
                elif e.is_decrease():
                    val = pytamer.tamer_expr_make_minus(self._env, converter.convert(e.fluent), converter.convert(e.value))
                    ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(e.fluent), val)
                else:
                    raise NotImplementedError
                expr = pytamer.tamer_expr_make_temporal_expression(self._env, self._tamer_start, ass)
                expressions.append(expr)
            expr = pytamer.tamer_expr_make_assign(self._env, pytamer.tamer_expr_make_duration_anchor(self._env),
                                                  pytamer.tamer_expr_make_integer_constant(self._env, 1))
            expressions.append(expr)
            se = action.simulated_effect
            if se is not None:
                simulated_effects.append(self._convert_simulated_effect(converter, problem, action,
                                                                        up.model.StartTiming(), se))
        elif isinstance(action, up.model.DurativeAction):
            for i, lc in action.conditions.items():
                for c in lc:
                    expr = pytamer.tamer_expr_make_temporal_expression(self._env,
                                                                       self._convert_interval(i),
                                                                       converter.convert(c))
                    expressions.append(expr)
            for t, le in action.effects.items():
                for e in le:
                    assert not e.is_conditional()
                    if e.is_assignment():
                        ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(e.fluent), converter.convert(e.value))
                    elif e.is_increase():
                        val = pytamer.tamer_expr_make_plus(self._env, converter.convert(e.fluent), converter.convert(e.value))
                        ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(e.fluent), val)
                    elif e.is_decrease():
                        val = pytamer.tamer_expr_make_minus(self._env, converter.convert(e.fluent), converter.convert(e.value))
                        ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(e.fluent), val)
                    else:
                        raise NotImplementedError
                    expr = pytamer.tamer_expr_make_temporal_expression(self._env,
                                                                       self._convert_timing(t),
                                                                       ass)
                    expressions.append(expr)
            for t, se in action.simulated_effects.items():
                simulated_effects.append(self._convert_simulated_effect(converter, problem, action, t, se))
            expressions.append(self._convert_duration(converter, action.duration))
        else:
            raise NotImplementedError
        return pytamer.tamer_action_new(self._env, action.name, [], params, expressions, simulated_effects)

    def _convert_problem(self, problem: 'up.model.Problem') -> Tuple[pytamer.tamer_problem, Converter]:
        user_types = []
        user_types_map = {}
        instances = []
        instances_map = {}
        for ut in problem.user_types:
            name = cast(up.model.types._UserType, ut).name
            new_ut = pytamer.tamer_user_type_new(self._env, name)
            user_types.append(new_ut)
            user_types_map[ut] = new_ut
            for obj in problem.objects(ut):
                new_obj = pytamer.tamer_instance_new(self._env, obj.name, user_types_map[ut])
                instances.append(new_obj)
                instances_map[obj] = new_obj

        fluents = []
        fluents_map = {}
        static_fluents = problem.get_static_fluents()
        for f in problem.fluents:
            if f not in static_fluents:
                new_f = self._convert_fluent(f, user_types_map)
                fluents.append(new_f)
                fluents_map[f] = new_f

        expressions = []
        converter = Converter(self._env, problem, fluents_map, {}, instances_map)
        constants_assignments = {}
        for k, v in problem.initial_values.items():
            if k.type.is_real_type() and v.is_int_constant():
                v = problem.environment.expression_manager.Real(Fraction(v.constant_value()))
            if k.fluent() not in static_fluents:
                ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(k), converter.convert(v))
                expr = pytamer.tamer_expr_make_temporal_expression(self._env, self._tamer_start, ass)
                expressions.append(expr)
            else:
                if k.fluent() not in constants_assignments:
                    constants_assignments[k.fluent()] = []
                constants_assignments[k.fluent()].append(([converter.convert(ki) for ki in k.args],
                                                          converter.convert(v)))

        constants = []
        constants_map = {}
        for c in static_fluents:
            new_c = self._convert_constant(c, constants_assignments[c], user_types_map)
            constants.append(new_c)
            constants_map[c] = new_c

        converter = Converter(self._env, problem, fluents_map, constants_map, instances_map)

        actions = []
        for a in problem.actions:
            new_a = self._convert_action(problem, a, fluents_map, constants_map,
                                         user_types_map, instances_map)
            actions.append(new_a)

        for g in problem.goals:
            expr = pytamer.tamer_expr_make_temporal_expression(self._env, self._tamer_end,
                                                               converter.convert(g))
            expressions.append(expr)
        for t, le in problem.timed_effects.items():
            t = self._convert_timing(t)
            for e in le:
                assert not e.is_conditional() and e.is_assignment()
                ass = pytamer.tamer_expr_make_assign(self._env, converter.convert(e.fluent),
                                                     converter.convert(e.value))
                expr = pytamer.tamer_expr_make_temporal_expression(self._env, t, ass)
                expressions.append(expr)
        for i, l in problem.timed_goals.items():
            i = self._convert_interval(i)
            for g in l:
                expr = pytamer.tamer_expr_make_temporal_expression(self._env, i,
                                                                   converter.convert(g))
                expressions.append(expr)

        return pytamer.tamer_problem_new(self._env, actions, fluents, constants, instances, user_types, expressions), converter

    def _to_up_plan(self, problem: 'up.model.Problem',
                    ttplan: Optional[pytamer.tamer_ttplan]) -> Optional['up.plans.Plan']:
        if ttplan is None:
            return None
        converter = Converter(self._env, problem)
        actions = []
        for s in pytamer.tamer_ttplan_get_steps(ttplan):
            taction = pytamer.tamer_ttplan_step_get_action(s)
            start = Fraction(pytamer.tamer_ttplan_step_get_start_time(s))
            duration = None
            name = pytamer.tamer_action_get_name(taction)
            action = problem.action(name)
            if isinstance(action, up.model.DurativeAction):
                duration = Fraction(pytamer.tamer_ttplan_step_get_duration(s))
            params = []
            for p in pytamer.tamer_ttplan_step_get_parameters(s):
                params.append(converter.convert_back(p))
            actions.append((start, up.plans.ActionInstance(action, tuple(params)), duration))
        if problem.kind.has_continuous_time():
            return up.plans.TimeTriggeredPlan(actions, problem.environment)
        else:
            return up.plans.SequentialPlan([a[1] for a in actions], problem.environment)

    def _solve_classical_problem(self, tproblem: pytamer.tamer_problem,
                                 heuristic_fun) -> Tuple[Optional[pytamer.tamer_ttplan], float]:
        start = time.time()
        potplan = pytamer.tamer_do_tsimple_planning(tproblem, heuristic_fun)
        solving_time = time.time() - start
        if pytamer.tamer_potplan_is_error(potplan) == 1:
            return None, solving_time
        ttplan = pytamer.tamer_ttplan_from_potplan(potplan)
        return ttplan, solving_time

    def _convert_plan(self, tproblem: pytamer.tamer_problem, plan: 'up.plans.Plan') -> pytamer.tamer_ttplan:
        actions_map = {}
        for a in pytamer.tamer_problem_get_actions(tproblem):
            actions_map[pytamer.tamer_action_get_name(a)] = a
        instances_map = {}
        for i in pytamer.tamer_problem_get_instances(tproblem):
            instances_map[pytamer.tamer_instance_get_name(i)] = i
        ttplan = pytamer.tamer_ttplan_new(self._env)
        steps: List[Tuple[Fraction, 'up.plans.ActionInstance', Optional[Fraction]]] = []
        if isinstance(plan, up.plans.SequentialPlan):
            steps = [(Fraction(i*2), a, Fraction(1)) for i, a in enumerate(plan.actions)]
        elif isinstance(plan, up.plans.TimeTriggeredPlan):
            steps = plan.timed_actions
        else:
            raise NotImplementedError
        for start, ai, duration in steps:
            if duration is None:
                duration = 1
            action = actions_map[ai.action.name]
            params = []
            for p in ai.actual_parameters:
                if p.is_object_exp():
                    i = instances_map[p.object().name]
                    params.append(pytamer.tamer_expr_make_instance_reference(self._env, i))
                elif p.is_true():
                    params.append(pytamer.tamer_expr_make_true(self._env))
                elif p.is_false():
                    params.append(pytamer.tamer_expr_make_false(self._env))
                elif p.is_int_constant():
                    params.append(pytamer.tamer_expr_make_integer_constant(self._env, p.constant_value()))
                elif p.is_real_constant():
                    f = p.constant_value()
                    n = f.numerator
                    d = f.denominator
                    params.append(pytamer.tamer_expr_make_rational_constant(self._env, n, d))
                else:
                    raise NotImplementedError
            step = pytamer.tamer_ttplan_step_new(str(start), action, params, str(duration), \
                                                 pytamer.tamer_expr_make_true(self._env))
            pytamer.tamer_ttplan_add_step(ttplan, step)
        return ttplan

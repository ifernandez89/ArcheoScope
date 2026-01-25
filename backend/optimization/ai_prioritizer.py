#!/usr/bin/env python3
"""
AI-Driven Computation Prioritizer for ArcheoScope
Intelligently prioritizes and schedules computations based on AI models
"""

import time
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError

logger = logging.getLogger(__name__)

class ComputationPriority(Enum):
    CRITICAL = "critical"      # Must execute
    HIGH = "high"             # Important for accuracy
    MEDIUM = "medium"          # Nice to have
    LOW = "low"               # Optional

@dataclass
class ComputationTask:
    """Represents a single computation task"""
    name: str
    function: Callable
    priority: ComputationPriority
    estimated_time_ms: float
    actual_time_ms: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class ExecutionPlan:
    """Execution plan for computations"""
    tasks: List[ComputationTask]
    total_estimated_time_ms: float
    time_budget_ms: float
    optimization_strategy: str
    ai_confidence: float

class AIComputationPrioritizer:
    """
    AI-driven computation prioritization system
    """
    
    def __init__(self):
        """Initialize AI prioritizer with learning models"""
        
        # Learning data
        self.performance_history = {}
        self.success_patterns = {}
        self.environment_profiles = {}
        
        # AI models (simplified for now)
        self.priority_model = self._load_priority_model()
        self.time_estimation_model = self._load_time_estimation_model()
        
        # Thread pool for parallel execution
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Cache for execution plans
        self.plan_cache = {}
        
        logger.info("🧠 AIComputationPrioritizer initialized with learning models")
    
    def create_execution_plan(self, computations: Dict[str, Dict[str, Any]], 
                             context: Dict[str, Any], 
                             time_budget_ms: float) -> ExecutionPlan:
        """
        Create optimized execution plan using AI prioritization
        """
        
        start_time = time.time()
        
        try:
            # Generate cache key
            cache_key = self._generate_plan_key(computations, context, time_budget_ms)
            
            # Check cache
            if cache_key in self.plan_cache:
                cached_plan = self.plan_cache[cache_key]
                logger.debug(f"🎯 Using cached execution plan")
                return cached_plan
            
            # Create tasks from computations
            tasks = self._create_tasks(computations, context)
            
            # AI prioritization
            prioritized_tasks = self._ai_prioritize_tasks(tasks, context, time_budget_ms)
            
            # Optimize for time budget
            optimized_tasks = self._optimize_for_time_budget(prioritized_tasks, time_budget_ms)
            
            # Create execution plan
            total_estimated_time = sum(task.estimated_time_ms for task in optimized_tasks)
            
            plan = ExecutionPlan(
                tasks=optimized_tasks,
                total_estimated_time_ms=total_estimated_time,
                time_budget_ms=time_budget_ms,
                optimization_strategy=self._determine_strategy(optimized_tasks, time_budget_ms),
                ai_confidence=self._calculate_ai_confidence(optimized_tasks, context)
            )
            
            # Cache plan
            plan_creation_time = (time.time() - start_time) * 1000
            if plan_creation_time < 100:  # Only cache if plan creation is fast
                self.plan_cache[cache_key] = plan
            
            logger.info(f"📋 AI execution plan created: {len(optimized_tasks)} tasks, "
                       f"{total_estimated_time:.1f}ms estimated, {plan.ai_confidence:.2f} confidence")
            
            return plan
            
        except Exception as e:
            logger.error(f"Error creating AI execution plan: {e}")
            return self._create_fallback_plan(computations, time_budget_ms)
    
    def execute_plan(self, plan: ExecutionPlan, parallel: bool = True) -> Dict[str, Any]:
        """
        Execute computation plan with time budget enforcement
        """
        
        start_time = time.time()
        results = {}
        
        try:
            logger.info(f"🚀 Executing plan: {plan.optimization_strategy} strategy, "
                       f"{plan.time_budget_ms}ms budget")
            
            if parallel and plan.optimization_strategy == "parallel":
                results = self._execute_parallel(plan, start_time)
            else:
                results = self._execute_sequential(plan, start_time)
            
            # Update learning models
            self._update_learning_models(plan, results, start_time)
            
            execution_time = (time.time() - start_time) * 1000
            logger.info(f"✅ Plan execution completed: {execution_time:.1f}ms, "
                       f"{len([r for r in results.values() if r is not None])} successful")
            
            return results
            
        except Exception as e:
            logger.error(f"Error executing plan: {e}")
            return self._create_fallback_results(plan)
    
    def _create_tasks(self, computations: Dict[str, Dict[str, Any]], 
                     context: Dict[str, Any]) -> List[ComputationTask]:
        """Create computation tasks from computation definitions"""
        
        tasks = []
        
        for name, comp_def in computations.items():
            # Estimate time using AI model
            estimated_time = self._estimate_execution_time(name, comp_def, context)
            
            # Determine priority using AI model
            priority = self._determine_priority(name, comp_def, context)
            
            task = ComputationTask(
                name=name,
                function=comp_def['function'],
                priority=priority,
                estimated_time_ms=estimated_time,
                dependencies=comp_def.get('dependencies', [])
            )
            
            tasks.append(task)
        
        return tasks
    
    def _ai_prioritize_tasks(self, tasks: List[ComputationTask], 
                            context: Dict[str, Any], time_budget_ms: float) -> List[ComputationTask]:
        """Use AI to prioritize tasks"""
        
        # Calculate priority scores for each task
        scored_tasks = []
        
        for task in tasks:
            # AI-based scoring
            score = self._calculate_priority_score(task, context, time_budget_ms)
            
            scored_tasks.append((task, score))
        
        # Sort by score (descending)
        scored_tasks.sort(key=lambda x: x[1], reverse=True)
        
        # Update task priorities based on scores
        prioritized_tasks = []
        for task, score in scored_tasks:
            # Update priority based on score percentile
            if score > 0.8:
                task.priority = ComputationPriority.CRITICAL
            elif score > 0.6:
                task.priority = ComputationPriority.HIGH
            elif score > 0.4:
                task.priority = ComputationPriority.MEDIUM
            else:
                task.priority = ComputationPriority.LOW
            
            prioritized_tasks.append(task)
        
        return prioritized_tasks
    
    def _calculate_priority_score(self, task: ComputationTask, 
                                 context: Dict[str, Any], time_budget_ms: float) -> float:
        """Calculate AI priority score for task"""
        
        # Base score from priority
        priority_scores = {
            ComputationPriority.CRITICAL: 1.0,
            ComputationPriority.HIGH: 0.7,
            ComputationPriority.MEDIUM: 0.4,
            ComputationPriority.LOW: 0.1
        }
        
        base_score = priority_scores[task.priority]
        
        # Environmental adjustment
        env_factor = self._get_environmental_factor(task.name, context)
        
        # Time efficiency factor
        time_efficiency = min(task.estimated_time_ms / time_budget_ms, 1.0)
        time_factor = 1.0 - (time_efficiency * 0.3)  # Penalize very slow tasks
        
        # Historical success factor
        success_factor = self._get_historical_success_factor(task.name, context)
        
        # Combined score
        final_score = base_score * env_factor * time_factor * success_factor
        
        return min(final_score, 1.0)
    
    def _get_environmental_factor(self, task_name: str, context: Dict[str, Any]) -> float:
        """Get environmental factor for task"""
        
        env_type = context.get('environment_type', 'unknown')
        
        # Environment-specific importance factors
        env_factors = {
            'desert': {
                'thermal_analysis': 1.2,
                'sar_processing': 1.1,
                'ndvi_analysis': 0.8,
                'default': 1.0
            },
            'forest': {
                'lidar_processing': 1.3,
                'ndvi_analysis': 1.2,
                'thermal_analysis': 0.6,
                'default': 1.0
            },
            'shallow_sea': {
                'sonar_processing': 1.3,
                'magnetic_analysis': 1.2,
                'bathymetry_processing': 1.1,
                'default': 1.0
            },
            'glacier': {
                'thermal_analysis': 1.2,
                'sar_processing': 1.1,
                'elevation_analysis': 1.1,
                'default': 1.0
            }
        }
        
        env_config = env_factors.get(env_type, {'default': 1.0})
        
        for key, factor in env_config.items():
            if key in task_name.lower():
                return factor
        
        return env_config['default']
    
    def _get_historical_success_factor(self, task_name: str, context: Dict[str, Any]) -> float:
        """Get historical success factor from learning data"""
        
        env_type = context.get('environment_type', 'unknown')
        
        # Check historical success patterns
        if task_name in self.success_patterns:
            env_success = self.success_patterns[task_name].get(env_type, 0.5)
            return env_success
        
        # Default moderate success factor
        return 0.6
    
    def _optimize_for_time_budget(self, tasks: List[ComputationTask], 
                                 time_budget_ms: float) -> List[ComputationTask]:
        """Optimize task list for time budget"""
        
        # Simple greedy optimization
        optimized_tasks = []
        remaining_budget = time_budget_ms
        
        for task in tasks:
            if task.estimated_time_ms <= remaining_budget:
                optimized_tasks.append(task)
                remaining_budget -= task.estimated_time_ms
            elif task.priority == ComputationPriority.CRITICAL:
                # Keep critical tasks even if over budget
                optimized_tasks.append(task)
                logger.warning(f"⚠️ Critical task {task.name} exceeds remaining budget")
            else:
                logger.info(f"ℹ️ Skipping task {task.name} - exceeds time budget")
        
        return optimized_tasks
    
    def _execute_sequential(self, plan: ExecutionPlan, start_time: float) -> Dict[str, Any]:
        """Execute plan sequentially"""
        
        results = {}
        
        for task in plan.tasks:
            # Check time budget
            elapsed_ms = (time.time() - start_time) * 1000
            remaining_ms = plan.time_budget_ms - elapsed_ms
            
            if remaining_ms < task.estimated_time_ms:
                logger.warning(f"⏰ Time budget exceeded for task {task.name}")
                break
            
            # Execute task with timeout
            try:
                task_start = time.time()
                
                result = self.executor.submit(task.function).result(
                    timeout=min(remaining_ms * 0.9 / 1000, task.estimated_time_ms * 1.5 / 1000)
                )
                
                task.actual_time_ms = (time.time() - task_start) * 1000
                task.result = result
                
                results[task.name] = result
                
            except TimeoutError:
                logger.warning(f"⏱️ Task {task.name} timed out")
                task.error = "Timeout"
            except Exception as e:
                logger.error(f"❌ Task {task.name} failed: {e}")
                task.error = str(e)
        
        return results
    
    def _execute_parallel(self, plan: ExecutionPlan, start_time: float) -> Dict[str, Any]:
        """Execute plan in parallel where possible"""
        
        results = {}
        
        # Separate tasks by priority
        critical_tasks = [t for t in plan.tasks if t.priority == ComputationPriority.CRITICAL]
        other_tasks = [t for t in plan.tasks if t.priority != ComputationPriority.CRITICAL]
        
        # Execute critical tasks first
        for task in critical_tasks:
            try:
                task_start = time.time()
                result = self.executor.submit(task.function).result(
                    timeout=task.estimated_time_ms * 1.5 / 1000
                )
                
                task.actual_time_ms = (time.time() - task_start) * 1000
                task.result = result
                results[task.name] = result
                
            except Exception as e:
                logger.error(f"❌ Critical task {task.name} failed: {e}")
                task.error = str(e)
        
        # Execute other tasks in parallel
        if other_tasks:
            try:
                # Submit all remaining tasks
                future_to_task = {
                    self.executor.submit(task.function): task 
                    for task in other_tasks
                }
                
                # Collect results with timeout
                for future in future_to_task:
                    task = future_to_task[future]
                    
                    try:
                        result = future.result(timeout=task.estimated_time_ms * 1.5 / 1000)
                        task.result = result
                        results[task.name] = result
                        
                    except Exception as e:
                        logger.error(f"❌ Task {task.name} failed: {e}")
                        task.error = str(e)
                
            except Exception as e:
                logger.error(f"❌ Parallel execution failed: {e}")
        
        return results
    
    def _estimate_execution_time(self, task_name: str, comp_def: Dict[str, Any], 
                               context: Dict[str, Any]) -> float:
        """Estimate execution time using AI model"""
        
        # Base time estimates (ms)
        base_times = {
            'thermal_analysis': 200,
            'sar_processing': 300,
            'lidar_processing': 500,
            'magnetic_analysis': 150,
            'sonar_processing': 400,
            'bathymetry_processing': 250,
            'ndvi_analysis': 100,
            'elevation_analysis': 180,
            'default': 200
        }
        
        # Get base time
        base_time = base_times.get('default', 200)
        for key, time_val in base_times.items():
            if key in task_name.lower():
                base_time = time_val
                break
        
        # Environmental adjustment
        env_factor = self._get_time_environment_factor(context.get('environment_type', 'unknown'))
        
        # Size adjustment
        bounds = context.get('bounds', {})
        area_km2 = abs(bounds.get('lat_max', 0) - bounds.get('lat_min', 0)) * \
                  abs(bounds.get('lon_max', 0) - bounds.get('lon_min', 0)) * 111 * 111
        
        size_factor = min(area_km2 / 100, 3.0)  # Cap at 3x
        
        # Historical adjustment
        historical_factor = self._get_historical_time_factor(task_name, context)
        
        # Final estimate
        estimated_time = base_time * env_factor * size_factor * historical_factor
        
        return estimated_time
    
    def _get_time_environment_factor(self, env_type: str) -> float:
        """Get time factor for environment type"""
        
        factors = {
            'desert': 0.8,      # Faster in desert (clear signals)
            'forest': 1.5,     # Slower in forest (complex processing)
            'shallow_sea': 1.2,  # Moderate
            'glacier': 1.3,     # Slower (complex physics)
            'polar_ice': 1.4,   # Slower
            'deep_ocean': 1.1,   # Slightly slower
            'unknown': 1.0
        }
        
        return factors.get(env_type, 1.0)
    
    def _get_historical_time_factor(self, task_name: str, context: Dict[str, Any]) -> float:
        """Get historical time adjustment factor"""
        
        env_type = context.get('environment_type', 'unknown')
        
        if task_name in self.performance_history:
            env_history = self.performance_history[task_name].get(env_type, {})
            avg_time = env_history.get('avg_time_ms')
            
            if avg_time:
                # Compare with base time
                base_time = 200  # Default base time
                return avg_time / base_time
        
        return 1.0
    
    def _determine_priority(self, task_name: str, comp_def: Dict[str, Any], 
                           context: Dict[str, Any]) -> ComputationPriority:
        """Determine task priority using AI"""
        
        # Base priority from definition
        if 'priority' in comp_def:
            priority_str = comp_def['priority'].lower()
            if priority_str == 'critical':
                return ComputationPriority.CRITICAL
            elif priority_str == 'high':
                return ComputationPriority.HIGH
            elif priority_str == 'medium':
                return ComputationPriority.MEDIUM
            elif priority_str == 'low':
                return ComputationPriority.LOW
        
        # AI-based priority determination
        env_type = context.get('environment_type', 'unknown')
        
        # Environmental importance
        critical_tasks = {
            'desert': ['thermal_analysis', 'sar_processing'],
            'forest': ['lidar_processing', 'ndvi_analysis'],
            'shallow_sea': ['sonar_processing', 'magnetic_analysis'],
            'glacier': ['thermal_analysis', 'elevation_analysis']
        }
        
        if task_name in critical_tasks.get(env_type, []):
            return ComputationPriority.HIGH
        
        return ComputationPriority.MEDIUM
    
    def _determine_strategy(self, tasks: List[ComputationTask], time_budget_ms: float) -> str:
        """Determine execution strategy"""
        
        total_estimated = sum(task.estimated_time_ms for task in tasks)
        
        if total_estimated > time_budget_ms * 0.8:
            return "optimized"
        elif any(task.estimated_time_ms > 1000 for task in tasks):
            return "parallel"
        else:
            return "sequential"
    
    def _calculate_ai_confidence(self, tasks: List[ComputationTask], 
                                context: Dict[str, Any]) -> float:
        """Calculate AI confidence in execution plan"""
        
        # Base confidence
        confidence = 0.7
        
        # Historical success adjustment
        env_type = context.get('environment_type', 'unknown')
        success_rates = [self._get_historical_success_factor(t.name, context) for t in tasks]
        avg_success_rate = np.mean(success_rates) if success_rates else 0.5
        
        confidence *= (0.5 + avg_success_rate)
        
        # Time budget adjustment
        total_estimated = sum(task.estimated_time_ms for task in tasks)
        time_pressure = total_estimated / context.get('time_budget_ms', total_estimated)
        
        if time_pressure < 0.7:
            confidence *= 1.1  # Confident with ample time
        elif time_pressure > 0.9:
            confidence *= 0.8  # Less confident with tight time
        
        return min(confidence, 1.0)
    
    def _update_learning_models(self, plan: ExecutionPlan, results: Dict[str, Any], 
                               start_time: float):
        """Update AI learning models with execution results"""
        
        execution_time = (time.time() - start_time) * 1000
        env_type = plan.tasks[0].function.__globals__.get('environment_type', 'unknown') if plan.tasks else 'unknown'
        
        for task in plan.tasks:
            if task.name in results:
                # Update performance history
                if task.name not in self.performance_history:
                    self.performance_history[task.name] = {}
                
                if env_type not in self.performance_history[task.name]:
                    self.performance_history[task.name][env_type] = {
                        'count': 0,
                        'total_time': 0,
                        'successes': 0
                    }
                
                history = self.performance_history[task.name][env_type]
                history['count'] += 1
                history['total_time'] += task.actual_time_ms or 0
                history['successes'] += 1
                
                # Update averages
                history['avg_time_ms'] = history['total_time'] / history['count']
                history['success_rate'] = history['successes'] / history['count']
    
    def _generate_plan_key(self, computations: Dict[str, Dict[str, Any]], 
                          context: Dict[str, Any], time_budget_ms: float) -> str:
        """Generate cache key for execution plan"""
        
        comp_keys = sorted(computations.keys())
        env_type = context.get('environment_type', 'unknown')
        
        return f"plan_{env_type}_{time_budget_ms}_{hash(str(comp_keys)) % 10000}"
    
    def _load_priority_model(self):
        """Load AI priority model (simplified)"""
        return "simplified_priority_model"
    
    def _load_time_estimation_model(self):
        """Load AI time estimation model (simplified)"""
        return "simplified_time_model"
    
    def _create_fallback_plan(self, computations: Dict[str, Any], time_budget_ms: float) -> ExecutionPlan:
        """Create fallback execution plan"""
        
        tasks = []
        for name, comp_def in computations.items():
            task = ComputationTask(
                name=name,
                function=comp_def['function'],
                priority=ComputationPriority.MEDIUM,
                estimated_time_ms=200  # Default estimate
            )
            tasks.append(task)
        
        return ExecutionPlan(
            tasks=tasks,
            total_estimated_time_ms=len(tasks) * 200,
            time_budget_ms=time_budget_ms,
            optimization_strategy="fallback",
            ai_confidence=0.3
        )
    
    def _create_fallback_results(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Create fallback results"""
        
        results = {}
        for task in plan.tasks:
            results[task.name] = None
        
        return results

# Global instance
ai_prioritizer = AIComputationPrioritizer()

def create_optimized_execution_plan(computations: Dict[str, Dict[str, Any]], 
                                   context: Dict[str, Any], 
                                   time_budget_ms: float) -> ExecutionPlan:
    """Create optimized execution plan using AI prioritization"""
    return ai_prioritizer.create_execution_plan(computations, context, time_budget_ms)

def execute_optimized_plan(plan: ExecutionPlan, parallel: bool = True) -> Dict[str, Any]:
    """Execute optimized plan with AI monitoring"""
    return ai_prioritizer.execute_plan(plan, parallel)
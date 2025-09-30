from typing import List, Dict, Optional, Any
import random
from .models import Component
from sqlalchemy.orm import Session

class AIRecommendationEngine:
    """Motor de IA para generar recomendaciones de componentes de PC."""
    
    def __init__(self, db: Session):
        self.db = db
        
        # Pesos para diferentes tipos de uso
        self.usage_weights = {
            "gaming": {
                "cpu": 0.25, "gpu": 0.35, "ram": 0.15, 
                "storage": 0.10, "motherboard": 0.10, "psu": 0.05
            },
            "office": {
                "cpu": 0.20, "gpu": 0.10, "ram": 0.20, 
                "storage": 0.25, "motherboard": 0.15, "psu": 0.10
            },
            "design": {
                "cpu": 0.30, "gpu": 0.30, "ram": 0.15, 
                "storage": 0.10, "motherboard": 0.10, "psu": 0.05
            },
            "development": {
                "cpu": 0.30, "gpu": 0.15, "ram": 0.25, 
                "storage": 0.15, "motherboard": 0.10, "psu": 0.05
            }
        }
        
    def _calculate_budget_distribution(self, budget: float, usage_type: str) -> Dict[str, float]:
        """Calcula la distribución del presupuesto según el tipo de uso."""
        if usage_type not in self.usage_weights:
            # Usar distribución por defecto si el tipo de uso no está definido
            usage_type = "gaming"
            
        distribution = {}
        for component_type, weight in self.usage_weights[usage_type].items():
            distribution[component_type] = budget * weight
            
        return distribution
    
    def _adjust_budget_for_preferences(self, budget_distribution: Dict[str, float], 
                                      preferences: Dict[str, bool]) -> Dict[str, float]:
        """Ajusta la distribución del presupuesto según las preferencias del usuario."""
        if not preferences:
            return budget_distribution
            
        adjusted_distribution = budget_distribution.copy()
        
        # Ajustar presupuesto basado en preferencias
        if preferences.get("prefer_performance", False):
            # Aumentar presupuesto para CPU y GPU
            total_increase = budget_distribution["motherboard"] * 0.2 + budget_distribution["psu"] * 0.2
            adjusted_distribution["cpu"] += total_increase * 0.5
            adjusted_distribution["gpu"] += total_increase * 0.5
            adjusted_distribution["motherboard"] -= budget_distribution["motherboard"] * 0.2
            adjusted_distribution["psu"] -= budget_distribution["psu"] * 0.2
            
        if preferences.get("prefer_storage", False):
            # Aumentar presupuesto para almacenamiento
            total_increase = budget_distribution["psu"] * 0.1
            adjusted_distribution["storage"] += total_increase
            adjusted_distribution["psu"] -= total_increase
            
        if preferences.get("prefer_silence", False):
            # Aumentar presupuesto para PSU (fuentes más silenciosas)
            total_increase = budget_distribution["gpu"] * 0.1
            adjusted_distribution["psu"] += total_increase
            adjusted_distribution["gpu"] -= total_increase
            
        return adjusted_distribution
    
    def _select_components_by_budget(self, budget_distribution: Dict[str, float]) -> Dict[str, Component]:
        """Selecciona componentes según el presupuesto asignado para cada tipo."""
        selected_components = {}
        
        for component_type, budget in budget_distribution.items():
            # Obtener componentes del tipo específico
            components = self.db.query(Component).filter(Component.type == component_type).all()
            
            # Filtrar componentes dentro del presupuesto (con un margen del 10%)
            affordable_components = [c for c in components if c.price <= budget * 1.1]
            
            if affordable_components:
                # Ordenar por rendimiento y seleccionar el mejor dentro del presupuesto
                best_component = max(affordable_components, 
                                    key=lambda c: c.performance_score if c.performance_score else 0)
                selected_components[component_type] = best_component
            else:
                # Si no hay componentes asequibles, seleccionar el más barato
                if components:
                    cheapest = min(components, key=lambda c: c.price)
                    selected_components[component_type] = cheapest
        
        return selected_components
    
    def _estimate_performance_score(self, components: Dict[str, Component]) -> float:
        """Estima la puntuación de rendimiento general del sistema."""
        if not components:
            return 0.0
            
        # Pesos para cada componente en la puntuación final
        performance_weights = {
            "cpu": 0.35,
            "gpu": 0.35,
            "ram": 0.15,
            "storage": 0.05,
            "motherboard": 0.05,
            "psu": 0.05
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for component_type, component in components.items():
            if component_type in performance_weights:
                weight = performance_weights[component_type]
                score = component.performance_score if component.performance_score else 50.0  # Valor por defecto
                total_score += score * weight
                total_weight += weight
                
        if total_weight > 0:
            return total_score / total_weight
        return 0.0
    
    def _check_compatibility(self, components: Dict[str, Component]) -> Dict:
        """Verifica la compatibilidad entre los componentes seleccionados."""
        issues = []
        compatible = True
        
        # Verificar si tenemos los componentes necesarios
        required_components = ["cpu", "motherboard", "ram", "storage", "psu"]
        for req in required_components:
            if req not in components:
                issues.append(f"Falta componente requerido: {req}")
                compatible = False
        
        if not compatible:
            return {
                "compatible": False,
                "message": "Faltan componentes esenciales",
                "issues": issues,
                "compatibility_score": 0.0
            }
        
        # Verificar compatibilidad CPU-Motherboard
        if "cpu" in components and "motherboard" in components:
            cpu = components["cpu"]
            motherboard = components["motherboard"]
            
            # Extraer socket de CPU y motherboard de las especificaciones
            cpu_socket = None
            mb_socket = None
            
            for spec in cpu.specifications:
                if spec.name.lower() == "socket":
                    cpu_socket = spec.value
                    
            for spec in motherboard.specifications:
                if spec.name.lower() == "socket":
                    mb_socket = spec.value
            
            if cpu_socket and mb_socket and cpu_socket != mb_socket:
                issues.append(f"Socket de CPU ({cpu_socket}) no compatible con placa base ({mb_socket})")
                compatible = False
        
        # Calcular puntuación de compatibilidad
        compatibility_score = 100.0
        if issues:
            compatibility_score -= len(issues) * 25.0
            compatibility_score = max(compatibility_score, 0.0)
        
        return {
            "compatible": compatible,
            "message": "Componentes compatibles" if compatible else "Problemas de compatibilidad detectados",
            "issues": issues,
            "compatibility_score": compatibility_score
        }
    
    def generate_recommendation(self, budget: float, usage_type: str, 
                               preferences: Optional[Dict[str, bool]] = None) -> Dict:
        """Genera una recomendación de componentes basada en presupuesto y preferencias."""
        # Calcular distribución de presupuesto
        budget_distribution = self._calculate_budget_distribution(budget, usage_type)
        
        # Ajustar según preferencias
        if preferences:
            budget_distribution = self._adjust_budget_for_preferences(budget_distribution, preferences)
        
        # Seleccionar componentes iniciales
        selected_components = self._select_components_by_budget(budget_distribution)
        
        # Verificar compatibilidad
        compatibility_result = self._check_compatibility(selected_components)
        
        # Calcular precio total
        total_price = sum(component.price for component in selected_components.values())
        
        # Calcular puntuación de rendimiento
        performance_score = self._estimate_performance_score(selected_components)
        
        # Preparar resultado
        component_list = list(selected_components.values())
        
        return {
            "components": component_list,
            "total_price": total_price,
            "performance_score": performance_score,
            "compatibility_score": compatibility_result["compatibility_score"],
            "compatibility_details": compatibility_result
        }

def get_ai_engine(db: Session) -> AIRecommendationEngine:
    """Función para obtener una instancia del motor de IA."""
    return AIRecommendationEngine(db)
import math
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Location:
    id: str
    lat: float
    lon: float

@dataclass
class Order:
    id: str
    location: Location
    weight: float
    priority: int  # 1 (High) to 5 (Low)

class BodaOptimizer:
    def __init__(self, hub_location: Location, max_capacity: float = 30.0):
        self.hub = hub_location
        self.max_capacity = max_capacity

    @staticmethod
    def haversine(loc1: Location, loc2: Location) -> float:
        """Calculate the great circle distance between two points in km."""
        R = 6371.0
        dlat = math.radians(loc2.lat - loc1.lat)
        dlon = math.radians(loc2.lon - loc1.lon)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(loc1.lat)) * \
            math.cos(math.radians(loc2.lat)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def optimize_route(self, orders: List[Order]) -> Dict:
        """
        Greedy Nearest Neighbor approach tailored for high-density urban boda-boda delivery.
        Includes capacity constraints and returns an optimized sequence.
        """
        if not orders:
            return {"route": [], "total_distance": 0}

        pending = orders[:]
        current_loc = self.hub
        route = []
        total_distance = 0.0
        current_load = 0.0

        while pending:
            # Filter orders that fit in remaining capacity
            available = [o for o in pending if current_load + o.weight <= self.max_capacity]
            
            if not available:
                # Return to hub to reload
                total_distance += self.haversine(current_loc, self.hub)
                current_loc = self.hub
                current_load = 0.0
                continue

            # Find nearest next stop among available orders
            next_order = min(
                available, 
                key=lambda o: (self.haversine(current_loc, o.location), o.priority)
            )
            
            dist = self.haversine(current_loc, next_order.location)
            total_distance += dist
            current_load += next_order.weight
            route.append(next_order.id)
            current_loc = next_order.location
            pending.remove(next_order)

        # Return to hub after last delivery
        total_distance += self.haversine(current_loc, self.hub)
        
        return {
            "route_sequence": route,
            "total_distance_km": round(total_distance, 2),
            "stops": len(route)
        }

if __name__ == "__main__":
    # Mock data for a high-density zone (e.g., Kampala Central or Nairobi CBD)
    hub = Location("HUB-01", 0.3476, 32.5825)
    optimizer = BodaOptimizer(hub)

    test_orders = [
        Order("ORD-001", Location("LOC-1", 0.3501, 32.5850), 5.0, 1),
        Order("ORD-002", Location("LOC-2", 0.3420, 32.5900), 12.0, 2),
        Order("ORD-003", Location("LOC-3", 0.3550, 32.5780), 8.0, 1),
        Order("ORD-004", Location("LOC-4", 0.3400, 32.5700), 10.0, 3),
    ]

    result = optimizer.optimize_route(test_orders)
    print(json.dumps(result, indent=4))
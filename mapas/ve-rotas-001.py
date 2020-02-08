from pyroutelib3 import Router # Import the router
router = Router("car") # Initialise it

start = router.findNode(lat=-15.80423, lon=-47.9526007) # Find start and end nodes
end = router.findNode(lat=-15.8055607, lon=-47.9515105)

status, route = router.doRoute(start, end) # Find the route - a list of OSM nodes
print(status)
print(route)

if status == 'success':
    routeLatLons = list(map(router.nodeLatLon, route)) # Get actual route coordinates


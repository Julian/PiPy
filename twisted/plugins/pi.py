from twisted.application.service import ServiceMaker
mux = ServiceMaker(
    name="Pi.Py Server Service",
    module="pi.tap",
    description="The Pi.Py Application Service",
    tapname="pi",
)

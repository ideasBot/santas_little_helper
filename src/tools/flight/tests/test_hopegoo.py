from unittest import TestCase
from src.tools.flight.flight_advanced import _parse_single_price
from bs4 import BeautifulSoup
from decimal import Decimal


class TestHopegoo(TestCase):
    one_way_trip_html = """
                <div class="styled__Body-meta___sc-bv4xxi-0 jAzkIQ">
                  <ul class="styled__Card-meta___sc-bv4xxi-1 dWoiwQ"><img
                      src="//file.40017.cn/iflight/common/img/pcaircompanylogo/SQ.png"
                      class="styled__Img-meta___sc-bv4xxi-3 jlGpdR">
                    <dl class="styled__AirInfo-meta___sc-bv4xxi-48 dTzsJf">
                      <dt class="styled__AirCompany-meta___sc-bv4xxi-5 KWvLS all_nowrap">Singapore Airlines</dt>
                      <dd class="styled__AirNo-meta___sc-bv4xxi-6 dvETLn all_nowrap">SQ806 Boeing 787</dd>
                      <dd class="styled__FlightDetail-meta___sc-bv4xxi-7 ksKMzq all_nowrap">Flight Details<svg
                          class="arrow_svg__icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="1em"
                          height="1em">
                          <defs>
                            <style></style>
                          </defs>
                          <path
                            d="M767.707 519.45L308.066 71.478l-52.012 50.732 407.574 397.21-407.542 397.21 51.975 50.733z">
                          </path>
                        </svg></dd>
                    </dl>
                    <div class="styled__TimeContainer-meta___sc-bv4xxi-49 gUesMO">
                      <div class="styled__TimeBox-meta___sc-bv4xxi-50 dYWoNw">
                        <p class="styled__Time-meta___sc-bv4xxi-8 fdloYC all_nowrap">16:55</p>
                        <p class="styled__Terminal-meta___sc-bv4xxi-9 OsrlU all_nowrap">SIN T3</p>
                      </div>
                      <div class="styled__FlightLine-meta___sc-bv4xxi-10 iUxuae"></div>
                      <div class="styled__TimeBox-meta___sc-bv4xxi-50 dYWoNw">
                        <p class="styled__Time-meta___sc-bv4xxi-8 fdloYC all_nowrap">23:00</p>
                        <p class="styled__Terminal-meta___sc-bv4xxi-9 OsrlU all_nowrap">PEK T3</p>
                      </div>
                    </div>
                    <p class="styled__Duration-meta___sc-bv4xxi-14 faaJsB">6h5m</p>
                    <div class="styled__PriceContainer-meta___sc-bv4xxi-53 fiRSGI all_nowrap">
                      <div class="styled__PriceBox-meta___sc-bv4xxi-45 cJFeNL"><em
                          class="styled__Currency-meta___sc-bv4xxi-16 kqsYkY">CNY</em><strong
                          class="styled__Price-meta___sc-bv4xxi-15 kMjffC"><span
                            class="num2Price__PriceText-meta___sc-1umktae-0 hhdVTA"> 1,284</span></strong></div>
                    </div><i class="styled__ProductExpand-meta___sc-bv4xxi-54 cjTTdY"><svg class="arrow_svg__icon"
                        viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em">
                        <defs>
                          <style></style>
                        </defs>
                        <path
                          d="M767.707 519.45L308.066 71.478l-52.012 50.732 407.574 397.21-407.542 397.21 51.975 50.733z">
                        </path>
                      </svg></i>
                  </ul>
                  <div class="MuiCollapse-root MuiCollapse-hidden" style="min-height: 0px;">
                    <div class="MuiCollapse-wrapper">
                      <div class="MuiCollapse-wrapperInner">
                        <div class="product-skeleton">
                          <div class="title">
                            <div width="50%" class="skeleton__SkeletonProd-meta___sc-112lugn-1 ibgOye"></div>
                            <div width="50%" class="skeleton__SkeletonProd-meta___sc-112lugn-1 ibgOye"></div>
                          </div>
                          <div width="100%" class="skeleton__SkeletonProd-meta___sc-112lugn-1 jDcWUy"></div>
                          <div width="100%" class="skeleton__SkeletonProd-meta___sc-112lugn-1 jDcWUy"></div>
                          <div width="100%" class="skeleton__SkeletonProd-meta___sc-112lugn-1 jDcWUy"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="MuiCollapse-root MuiCollapse-hidden" style="min-height: 0px;">
                    <div class="MuiCollapse-wrapper">
                      <div class="MuiCollapse-wrapperInner">
                        <div class="styled__Body-meta___sc-h304oe-0 ivJOJm">
                          <dl class="styled__Flight-meta___sc-h304oe-8 jwFluW">
                            <dt class="styled__AirInfo-meta___sc-h304oe-9 eCYbkg"><img
                                src="//file.40017.cn/iflight/common/img/pcaircompanylogo/SQ.png"
                                class="styled__Img-meta___sc-h304oe-1 jPWmBa">
                              <p class="styled__Air-meta___sc-h304oe-2 iWLPgQ">Singapore Airlines SQ806 6h5m</p>
                            </dt>
                            <dd class="styled__TimeLine-meta___sc-h304oe-10 PtMim">
                              <p class="styled__M-meta___sc-h304oe-3 dJSyZS all_nowrap">Jan 2</p>
                              <p class="styled__T-meta___sc-h304oe-4 fEWMEY">16:55</p><i type="d"
                                class="styled__Line-meta___sc-h304oe-5 cCIquM"></i>
                              <p class="styled__Code-meta___sc-h304oe-6 laTEvg">SIN</p>
                              <p class="styled__Others-meta___sc-h304oe-7 heQEJE">Changi Airport T3</p>
                            </dd>
                            <dd class="styled__TimeLine-meta___sc-h304oe-10 PtMim">
                              <p class="styled__M-meta___sc-h304oe-3 dJSyZS all_nowrap">Jan 2</p>
                              <p class="styled__T-meta___sc-h304oe-4 fEWMEY">23:00</p><i
                                class="styled__Line-meta___sc-h304oe-5 jGGQpC"></i>
                              <p class="styled__Code-meta___sc-h304oe-6 laTEvg">PEK</p>
                              <p class="styled__Others-meta___sc-h304oe-7 heQEJE">Beijing Capital International Airport
                                T3</p>
                            </dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="MuiCollapse-root MuiCollapse-hidden" style="min-height: 0px;">
                    <div class="MuiCollapse-wrapper">
                      <div class="MuiCollapse-wrapperInner"></div>
                    </div>
                  </div>
                </div>
"""

    rount_trip_html = """
                            <div class="styled__Body-meta___sc-bv4xxi-0 jAzkIQ">
                                <ul class="styled__Card-meta___sc-bv4xxi-1 dWoiwQ"><img
                                        src="//file.40017.cn/iflight/common/img/pcaircompanylogo/MU.png"
                                        class="styled__Img-meta___sc-bv4xxi-3 jlGpdR">
                                    <dl class="styled__AirInfo-meta___sc-bv4xxi-48 dTzsJf">
                                        <dt class="styled__AirCompany-meta___sc-bv4xxi-5 KWvLS all_nowrap">China Eastern
                                            Airlines</dt>
                                        <dd class="styled__AirNo-meta___sc-bv4xxi-6 dvETLn all_nowrap">MU5032 Airbus
                                            A320N</dd>
                                        <dd class="styled__FlightDetail-meta___sc-bv4xxi-7 ksKMzq all_nowrap">Flight
                                            Details<svg class="arrow_svg__icon" viewBox="0 0 1024 1024"
                                                xmlns="http://www.w3.org/2000/svg" width="1em" height="1em">
                                                <defs>
                                                    <style></style>
                                                </defs>
                                                <path
                                                    d="M767.707 519.45L308.066 71.478l-52.012 50.732 407.574 397.21-407.542 397.21 51.975 50.733z">
                                                </path>
                                            </svg></dd>
                                    </dl>
                                    <div class="styled__TimeContainer-meta___sc-bv4xxi-49 gUesMO">
                                        <div class="styled__TimeBox-meta___sc-bv4xxi-50 dYWoNw">
                                            <p class="styled__Time-meta___sc-bv4xxi-8 fdloYC all_nowrap">00:55</p>
                                            <p class="styled__Terminal-meta___sc-bv4xxi-9 OsrlU all_nowrap">SIN T3</p>
                                        </div>
                                        <div class="styled__FlightLine-meta___sc-bv4xxi-10 iUxuae"></div>
                                        <div class="styled__TimeBox-meta___sc-bv4xxi-50 dYWoNw">
                                            <p class="styled__Time-meta___sc-bv4xxi-8 fdloYC all_nowrap">07:10</p>
                                            <p class="styled__Terminal-meta___sc-bv4xxi-9 OsrlU all_nowrap">PKX </p>
                                        </div>
                                    </div>
                                    <p class="styled__Duration-meta___sc-bv4xxi-14 faaJsB">6h15m</p>
                                    <div class="styled__PriceContainer-meta___sc-bv4xxi-53 fiRSGI all_nowrap">
                                        <div class="styled__PriceBox-meta___sc-bv4xxi-45 cJFeNL"><em
                                                class="styled__Currency-meta___sc-bv4xxi-16 kqsYkY">CNY</em><strong
                                                class="styled__Price-meta___sc-bv4xxi-15 kMjffC"><span
                                                    class="num2Price__PriceText-meta___sc-1umktae-0 hhdVTA">
                                                    3,493</span></strong></div>
                                    </div><button
                                        class="button__BookBtn-meta___sc-8hy1r4-0 styled__Button-meta___sc-bv4xxi-40 euuYIP hiuwkS">Select</button>
                                </ul>
                                <div class="MuiCollapse-root MuiCollapse-hidden" style="min-height: 0px;">
                                    <div class="MuiCollapse-wrapper">
                                        <div class="MuiCollapse-wrapperInner">
                                            <div class="product-skeleton">
                                                <div class="title">
                                                    <div width="50%"
                                                        class="skeleton__SkeletonProd-meta___sc-112lugn-1 ibgOye"></div>
                                                    <div width="50%"
                                                        class="skeleton__SkeletonProd-meta___sc-112lugn-1 ibgOye"></div>
                                                </div>
                                                <div width="100%"
                                                    class="skeleton__SkeletonProd-meta___sc-112lugn-1 jDcWUy"></div>
                                                <div width="100%"
                                                    class="skeleton__SkeletonProd-meta___sc-112lugn-1 jDcWUy"></div>
                                                <div width="100%"
                                                    class="skeleton__SkeletonProd-meta___sc-112lugn-1 jDcWUy"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="MuiCollapse-root MuiCollapse-hidden" style="min-height: 0px;">
                                    <div class="MuiCollapse-wrapper">
                                        <div class="MuiCollapse-wrapperInner">
                                            <div class="styled__Body-meta___sc-h304oe-0 ivJOJm">
                                                <dl class="styled__Flight-meta___sc-h304oe-8 jwFluW">
                                                    <dt class="styled__AirInfo-meta___sc-h304oe-9 eCYbkg"><img
                                                            src="//file.40017.cn/iflight/common/img/pcaircompanylogo/MU.png"
                                                            class="styled__Img-meta___sc-h304oe-1 jPWmBa">
                                                        <p class="styled__Air-meta___sc-h304oe-2 iWLPgQ">China Eastern
                                                            Airlines MU5032 6h15m</p>
                                                    </dt>
                                                    <dd class="styled__TimeLine-meta___sc-h304oe-10 PtMim">
                                                        <p class="styled__M-meta___sc-h304oe-3 dJSyZS all_nowrap">Dec 25
                                                        </p>
                                                        <p class="styled__T-meta___sc-h304oe-4 fEWMEY">00:55</p><i
                                                            type="d" class="styled__Line-meta___sc-h304oe-5 cCIquM"></i>
                                                        <p class="styled__Code-meta___sc-h304oe-6 laTEvg">SIN</p>
                                                        <p class="styled__Others-meta___sc-h304oe-7 heQEJE">Changi
                                                            Airport T3</p>
                                                    </dd>
                                                    <dd class="styled__TimeLine-meta___sc-h304oe-10 PtMim">
                                                        <p class="styled__M-meta___sc-h304oe-3 dJSyZS all_nowrap">Dec 25
                                                        </p>
                                                        <p class="styled__T-meta___sc-h304oe-4 fEWMEY">07:10</p><i
                                                            class="styled__Line-meta___sc-h304oe-5 jGGQpC"></i>
                                                        <p class="styled__Code-meta___sc-h304oe-6 laTEvg">PKX</p>
                                                        <p class="styled__Others-meta___sc-h304oe-7 heQEJE">Beijing
                                                            Daxing International Airport </p>
                                                    </dd>
                                                </dl>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="MuiCollapse-root MuiCollapse-hidden" style="min-height: 0px;">
                                    <div class="MuiCollapse-wrapper">
                                        <div class="MuiCollapse-wrapperInner"></div>
                                    </div>
                                </div>
                            </div>
"""

    def test_parse_one_way_trip_price(self):
        price = _parse_single_price(
            BeautifulSoup(self.one_way_trip_html, "html.parser")
        )

        self.assertEqual(
            price.model_dump(),
            {
                "arrival_time": "23:00",
                "arrival_airport": "PEK T3",
                "carrier": "Singapore Airlines",
                "currency": "CNY",
                "departure_time": "16:55",
                "departure_airport": "SIN T3",
                "flight_duration": "16:55",
                "flight_number_and_model": "SQ806 Boeing 787",
                "price": Decimal("1284"),
            },
        )

    def test_parse_round_trip_price(self):
        price = _parse_single_price(BeautifulSoup(self.rount_trip_html, "html.parser"))

        self.assertEqual(
            price.model_dump(),
            {
                "carrier": "China Eastern Airlines",
                "flight_number_and_model": "MU5032 Airbus A320N",
                "departure_airport": "SIN T3",
                "departure_time": "00:55",
                "arrival_airport": "PKX",
                "arrival_time": "07:10",
                "flight_duration": "00:55",
                "currency": "CNY",
                "price": Decimal("3493"),
            },
        )

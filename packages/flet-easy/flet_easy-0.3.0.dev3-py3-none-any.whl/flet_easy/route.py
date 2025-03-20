import re
from collections import deque
from inspect import iscoroutinefunction
from re import Pattern, compile, escape
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from flet import ControlEvent, KeyboardEvent, Page, RouteChangeEvent, View, ViewPopEvent

from flet_easy.datasy import Datasy
from flet_easy.exceptions import LoginRequiredError, MidlewareError, RouteError
from flet_easy.extra import TYPE_PATTERNS, Msg, Redirect
from flet_easy.inheritance import Keyboardsy, Resizesy, Viewsy
from flet_easy.middleware import Middleware
from flet_easy.pagesy import MiddlewareRequest, Pagesy
from flet_easy.view_404 import page_404_fs


class FletEasyX:
    __compiled_patterns_cache: Dict[str, re.Pattern[str]] = {}

    def __init__(
        self,
        route_prefix: str,
        route_init: str,
        route_login: str,
        on_resize: bool,
        on_Keyboard: bool,
        secret_key: str,
        auto_logout: bool,
    ):
        self.__page_on_keyboard = Keyboardsy()

        self.__route_prefix = route_prefix
        self.__route_init = route_init
        self.__route_login = route_login
        self.__on_resize = on_resize
        self.__on_Keyboard = on_Keyboard

        self._pages = deque()
        self.__history_pages: Dict[str, View] = {}
        self.__view_404 = page_404_fs

        self.__page: Page = None
        self._page_404: Pagesy = None
        self._view_data: Callable[[Datasy], Viewsy] = None
        self._config_login: Callable[[Datasy], bool] = None
        self._view_config: Callable[[Datasy], None] = None
        self._config_event: Callable[[Datasy], None] = None
        self._middlewares_after: Optional[List[MiddlewareRequest]] = None
        self.__pagesy: Pagesy = None
        self._middlewares: Middleware = None

        self.__auto_logout = auto_logout
        self.__secret_key = secret_key
        self.__page_on_resize: Resizesy = None
        self._data: Datasy = Datasy(
            route_prefix="" if self.__route_prefix is None else self.__route_prefix,
            route_init=self.__route_init,
            route_login=self.__route_login,
            secret_key=self.__secret_key,
            auto_logout=self.__auto_logout,
            page_on_keyboard=self.__page_on_keyboard,
            go=self._go,
        )

    # -------- ---------[Handling 'flet' event]----------

    def __route_change(self, e: RouteChangeEvent):
        if self.__pagesy is None:
            if e.route == "/" and self.__route_init != "/":
                return self.__page.go(self.__route_init)

            self._go(e.route, True)
        else:
            self._view_append(e.route, self.__pagesy)
            self.__pagesy = None

    def __view_pop(self, e: ViewPopEvent):
        if len(self._data.history_routes) > 1:
            self._data.history_routes.pop()
            self._go(self._data.history_routes.pop())

    async def __on_keyboard(self, e: KeyboardEvent):
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            await self.__page_on_keyboard._run_controls()

    def __page_resize(self, e: ControlEvent):
        self.__page_on_resize.e = e

    def __disconnect(self, e):
        if self._data._login_done and self.__page.web:
            self.__page.pubsub.send_others_on_topic(
                self.__page.client_ip,
                Msg("updateLoginSessions", value=self._data._login_done),
            )

    # --------------[End of 'flet' event]------------

    # ------------ [ configuration when initializing 'flet' ]

    def __check_async(
        self, func: Callable[[Union[Datasy, Page]], Any], *args, result: bool = False, **kwargs
    ) -> Union[View, bool, None]:
        """Check if the function is async or not"""
        if func is None:
            return

        if iscoroutinefunction(func):
            res = self.__page.run_task(func, *args, **kwargs)

            if result:
                return res.result(5)
            else:
                return res
        else:
            return func(*args, **kwargs)

    def __config_datasy(self):
        """configure datasy"""
        self.__page_on_resize = Resizesy(self.__page)
        self._data.page = self.__page
        self._data.on_resize = self.__page_on_resize

        """Add the `View` configuration, to reuse on every page."""
        self._data.view = self.__check_async(self._view_data, self._data, result=True)

        if self.__route_login is not None:
            self._data._create_login()

    def _add_configuration_start(self, page: Page):
        """Add general settings to the pages."""
        self.__page = page
        self.__page.views.clear()
        self.__config_datasy()

        """ Add view configuration """
        self.__check_async(self._view_config, self.__page)

        """ Add configuration event """
        self.__check_async(self._config_event, self._data)

    # ------------[Initialization]----------

    def _run(self):
        """configure the route init"""
        if self.__route_init != "/" and self.__page.route == "/":
            self.__page.route = self.__route_init

        """ Executing charter events """
        self.__page.on_route_change = self.__route_change
        self.__page.on_view_pop = self.__view_pop
        self.__page.on_error = lambda e: print("Page error:", e.data)
        self.__page.on_disconnect = self.__disconnect

        """ activation of charter events """
        if self.__on_resize:
            self.__page.on_resize = self.__page_resize
        if self.__on_Keyboard:
            self.__page.on_keyboard_event = self.__on_keyboard

        self._go(self.__page.route, use_reload=True)

    # ---------------------------[Route controller]-------------------------------------

    def _view_append(self, route: str, pagesy: Pagesy) -> None:
        """Add a new page and update it."""

        # To make the page change faster.
        if len(self.__page.views) == 2:
            self.__page.views.remove(self.__page.views[1])

        view = self.__history_pages.get(route)

        if view is None:
            if callable(pagesy.view) and not isinstance(pagesy.view, type):
                view = self.__check_async(
                    pagesy.view, self._data, **self._data.url_params, result=True
                )
            elif isinstance(pagesy.view, type):
                view_class = pagesy.view(self._data, **self._data.url_params)
                view = self.__check_async(view_class.build, result=True)

            view.route = route

            if pagesy.cache:
                self.__history_pages[route] = view

        self.__page.views.append(view)
        self._data.history_routes.append(route)
        self.__page.update()

        if self._middlewares_after:
            for middleware in self._middlewares_after:
                self.__check_async(middleware.after_request)

        if pagesy._valid_middlewares_request():
            for middleware in pagesy._middlewares_request:
                self.__check_async(middleware.after_request)

    def __reload_datasy(
        self,
        pagesy: Pagesy,
        url_params: Dict[str, Any] = dict(),
    ):
        """Update `datasy` values when switching between pages."""
        self.__page.title = pagesy.title

        if not pagesy.share_data:
            self._data.share.clear()
        if self.__on_Keyboard:
            self._data.on_keyboard_event.clear()

        self._data.url_params = url_params
        self._data.route = pagesy.route

    def __execute_middleware(
        self, pagesy: Pagesy, url_params: Dict[str, Any], middleware_list: Middleware
    ) -> bool:
        if not middleware_list:
            return False

        self.__reload_datasy(pagesy, url_params)

        try:
            for middleware in middleware_list:
                res = (
                    self.__check_async(middleware.before_request, result=True)
                    if isinstance(middleware, MiddlewareRequest)
                    else self.__check_async(middleware, self._data, result=True)
                )

                if self._handle_middleware_result(res):
                    return True

            return False

        except Exception as e:
            raise MidlewareError(e)

    def _handle_middleware_result(self, result):
        """Helper method to handle middleware results"""
        if not result:
            return False

        if isinstance(result, Redirect):
            self._go(result.route)
            return True

        return False

    def __run_middlewares(
        self,
        route: str,
        middleware: Middleware,
        url_params: Dict[str, Any],
        pagesy: Pagesy,
        use_route_change: bool,
        use_reload: bool,
    ):
        """Controla los middleware de la aplicación en general y en cada una de las páginas."""

        if self.__execute_middleware(pagesy, url_params, middleware):
            return True

        if self.__execute_middleware(pagesy, url_params, pagesy.middleware):
            return True

        self.__reload_datasy(pagesy, url_params)
        if use_route_change:
            self._view_append(route, pagesy)
        else:
            if self.__page.route != route or use_reload:
                self.__pagesy = pagesy
            self.__page.go(route)

        return True

    def _go(self, route: str, use_route_change: bool = False, use_reload: bool = False):
        """Go to the route, if the route is not found, it will return a 404 page."""
        pg_404 = True

        for page in self._pages:
            route_math = self._verify_url(page.route, route, page.custom_params)
            if route_math is not None:
                pg_404 = False
                try:
                    if page.protected_route:
                        self.__check_protected_route(
                            page,
                            route,
                            route_math,
                            use_route_change,
                            use_reload,
                        )
                        break
                    else:
                        if self.__run_middlewares(
                            route,
                            self._middlewares,
                            route_math,
                            page,
                            use_route_change,
                            use_reload,
                        ):
                            break
                except Exception as e:
                    raise RouteError(e)
        if pg_404:
            page = self._page_404 or Pagesy(route, self.__view_404, "Flet-Easy 404")

            if page.route is None:
                page.route = route

            self.__reload_datasy(page)

            if use_route_change:
                self._view_append(page.route, page)
            else:
                if self.__page.route != route or use_reload:
                    self.__pagesy = page
                self.__page.go(page.route)

    def __check_protected_route(
        self, page: Pagesy, route: str, route_math: str, use_route_change: bool, use_reload: bool
    ):
        """Check if the route is protected and if it is, check if the user is logged in."""
        assert self.__route_login is not None, (
            "Configure the route of the login page, in the Flet-Easy class in the parameter (route_login)"
        )

        try:
            auth = self.__check_async(self._config_login, self._data, result=True)
        except Exception as e:
            raise LoginRequiredError(
                "Use async methods in the function decorated by 'login', to avoid conflicts.",
                e,
            )

        if auth:
            self.__reload_datasy(page, route_math)

            if use_route_change:
                self._view_append(route, page)

            else:
                if self.__page.route != route or use_reload:
                    self.__pagesy = page
                self.__page.go(route)

        else:
            self._go(self.__route_login)

    @classmethod
    def __compile_pattern(cls, pattern_parts: list[str]) -> Pattern[str]:
        pattern_key = "/".join(pattern_parts)
        if pattern_key not in cls.__compiled_patterns_cache:
            cls.__compiled_patterns_cache[pattern_key] = compile(f"^/{pattern_key}/?$")
        return cls.__compiled_patterns_cache[pattern_key]

    @classmethod
    def _verify_url(
        cls,
        url_pattern: str,
        url: str,
        custom_types: Optional[Dict[str, Callable[[str], Optional[bool]]]] = None,
    ) -> Optional[Dict[str, Optional[bool]]]:
        combined_patterns = {
            **TYPE_PATTERNS,
            **{k: (compile(r"[^/]+"), v) for k, v in (custom_types or {}).items()},
        }

        segments: list[Tuple[str, Callable[[str], Optional[bool]]]] = []
        pattern_parts: list[str] = []
        type_patterns: list[str] = []

        for segment in url_pattern.strip("/").split("/"):
            try:
                if segment == "":
                    continue

                if segment[0] in "<{" and segment[-1] in ">}":
                    name, type_ = (
                        segment[1:-1].split(":", 1) if ":" in segment else (segment[1:-1], "str")
                    )
                    type_patterns.append(type_)
                    regex_part, parser = combined_patterns[type_]
                    pattern_parts.append(f"({regex_part.pattern})")
                    segments.append((name, parser))
                else:
                    pattern_parts.append(escape(segment))
            except KeyError as e:
                raise ValueError(f"Unrecognized data type: {e}")

        if custom_types and type_ not in custom_types:
            raise ValueError(f"A custom data type is not being used: {custom_types.keys()}")

        pattern = cls.__compile_pattern(pattern_parts)
        match = pattern.fullmatch(url)
        if not match:
            return None

        result = {name: parser(match.group(i + 1)) for i, (name, parser) in enumerate(segments)}

        return None if None in result.values() else result

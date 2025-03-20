import asyncio
import flet as ft
from pyinstrument import Profiler, profile

#x = Profiler()


def navigation_change(e: ft.ControlEvent):
    index = e.control.selected_index

    if index == 0:
        e.page.go("/")
    elif index == 1:
        e.page.go("/2")


t = ft.View(
    navigation_bar=ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME),
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD),
        ],
        on_change=navigation_change,
    ),
    appbar=ft.AppBar(title=ft.Text("Test", size=50), bgcolor=ft.Colors.RED),
)


async def test(page: ft.Page):
    page.title = "Test"
    return 123


def xd(page: ft.Page):
    l = asyncio.get_event_loop()
    # l = page.loop
    # l.run_in_executor(None, test, page)
    l.run_until_complete(test(page))
    return 1


# @profile
def main(page: ft.Page):
    
    page.title = "Test"
    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.NONE,
            ios=ft.PageTransitionTheme.NONE,
            macos=ft.PageTransitionTheme.NONE,
            linux=ft.PageTransitionTheme.NONE,
            windows=ft.PageTransitionTheme.NONE,
        )
    )

    # x = page.run_task(xd).result()
    # xd(page)

    def route_change(e: ft.RouteChangeEvent):
        if e.route == "/":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Text("Test World!"),
                    ],
                    appbar=t.appbar,
                    navigation_bar=t.navigation_bar,
                )
            )

        elif e.route == "/2":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Text("Test-2 World!"),
                    ],
                    appbar=t.appbar,
                    navigation_bar=t.navigation_bar,
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go("/")
    """ page.window.close() """


if __name__ == "__main__":
    a = ft.app(target=main)
""" 
x.stop()
x.open_in_browser(timeline=True) """

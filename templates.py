from fasthtml.common import *

def friend_form(name: str, experience: str, cv_path: str, 
                skills: List[Dict]):
    return Div(
        A(
            "Home",
            href="/",
            cls="text-xl text-blue-500 mb-3"
        ),
        H1(
            "Add New Friend",
            cls="text-3xl font-bold text-gray-800 mb-3",
        ),
        Div(
            Form(
                Div(
                    Label(
                        "Name",
                        for_="name",
                        cls="block text-gray-700 font-medium mb-2",
                    ),
                    Input(
                        type="text",
                        id="name",
                        name="name",
                        cls="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                        required=True,
                        value=name
                    ),
                    cls="mb-4",
                ),
                Div(
                    Label(
                        "Experience (Years)",
                        for_="experience",
                        cls="block text-gray-700 font-medium mb-2",
                    ),
                    Input(
                        type="number",
                        id="experience",
                        name="experience",
                        cls="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                        required=True,
                        min=0,
                        value=experience
                    ),
                    cls="mb-4",
                ),
                Div(
                    Label(
                        "CV path",
                        for_="cv",
                        cls="block text-gray-700 font-medium mb-2",
                    ),
                    Input(
                        type="text",
                        id="cv",
                        name="cv",
                        cls="w-full p-3 border border-gray-300 rounded-md " +
                            "focus:outline-none focus:ring-2 focus:ring-blue-500",
                        value=cv_path
                    ),
                    cls="mb-4",
                ),
                Div(

                    Label(
                        "Skills / Tags",
                        for_="tags",
                        cls="block text-gray-700 font-medium mb-2",

                    ),
                    Select(
                        *[
                            Option(skl['name'], value=f"{skl['id']}", 
                                   selected=skl['selected']) for skl in skills
                        ],
                        id="tags",
                        name="tags",
                        cls="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                        multiple=True,
                        required=True,
                    ),
                    cls="mb-4",
                ),
                Div(

                    Button(
                        "Add Friend",
                        type="submit",
                        cls="w-full py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 " \
                            "focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    cls="mt-4",
                ),
                action="/newfriend" if id is None else f"/newfriend/{id}/update",
                method="POST",

            ),
            cls="bg-white p-6 rounded-lg shadow-md",
        ),
        cls="max-w-3xl mx-auto p-6 mt-4 mb-12"
    )
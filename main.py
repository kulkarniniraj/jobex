from fasthtml.common import *
from peewee import fn

from models import db, SkillTag, PersonSkill, PositionSkill
from models import Person, Position
from templates import friend_form, position_form

app, rt = fast_app(hdrs=[
    Script(src="https://cdn.tailwindcss.com"),
], default_hdrs=False, debug=True)



@rt('/')
def get():
    return Title("JobEx job reference manager"), Body(
        Div(
            H1("Job Reference Management",
               cls="text-3xl font-bold text-gray-800 mb-6"),
            get_friends_div(),
            get_jobs_div(),
            get_skill_dev(),
            cls="max-w-7xl mx-auto py-6 px-64"),
        cls='bg-gray-100'
    )

##############################################################################
def get_friends_div():
    """
    Get div of all friends for home page
    """
    friends = (Person
               .select(Person, PersonSkill, SkillTag)
               .join(PersonSkill)
               .join(SkillTag))
    print(friends)
    frnd_dict = {
        f.id: {
            'name': f.name,
            'skills': [
                sk.skill.name for sk in f.skills
            ],
            'experience': f.experience
        }
        for f in friends
    }

    print(frnd_dict)

    return Div(
        H2("Friends", cls="text-2xl font-semibold text-gray-800 mb-4"),
        *[
            Div(
                Div(
                    Span(v['name'], cls="font-medium text-gray-700"),
                    Span("Skills: " + ', '.join(v['skills']),
                         cls="text-sm text-gray-500"),
                    Span(f"Experience: {v['experience']} years",
                         cls="text-sm text-gray-500"),
                    cls="flex space-x-4"
                ),
                Div(
                    A("Edit", href=f"/newfriend/{k}/edit", cls="text-blue-600 hover:text-blue-800"),
                    A("Delete", href="#", cls="text-red-600 hover:text-red-800"),
                    cls="space-x-2"
                ),
                cls="flex justify-between flex-col mb-4",
                id=f"{k}"
            )
            for k,v in frnd_dict.items()
        ],
        
        Div(
            A(
                " + Add Friend ",
                href="/newfriend",
                cls="text-green-600 hover:text-green-800"
            ),
            cls=""
        ),
        cls="bg-white p-6 rounded-lg shadow-md mb-6 max-h-96 overflow-y-scroll"
    )

def o_get_newfriend(name = '', experience = '', cv_path = '', skills_in = [], 
                    id = None):
    """
    Get Add/Update Page
    """
    skills = [{
        'name': skl.name,
        'id': skl.id,
        'selected': skl.id in skills_in} for skl in 
            SkillTag.select().order_by(fn.Lower(SkillTag.name))]
    print(skills_in)
    return friend_form(id, name, experience, cv_path, skills)

@rt('/newfriend')
def get():
    """
    Render form for adding new friend
    """
    return o_get_newfriend()

@rt('/newfriend')
def post(name: str, experience: int, cv: str, tags: list[str]):
    """
    Post route for adding new friend
    """
    print(f'{name=} {experience=} {cv=} {tags=}')
    print()
    friend = Person(name=name, experience=experience, cv_location=cv)
    friend.save()

    skills = SkillTag.select().where(SkillTag.id.in_(tags))
    for skill in skills:
        print(skill.id, skill.name)

    for skill in skills:
        PersonSkill(person=friend, skill=skill).save()

    return Redirect("/")

@rt('/newfriend/{id}/edit')
def get(id: int):
    """
    Get edit form for friend
    """
    frnd = Person.get_by_id(id)
    skills = PersonSkill.select().where(PersonSkill.person == id)
    return o_get_newfriend(frnd.name, frnd.experience, frnd.cv_location, 
                           [sk.skill.id for sk in skills], id = id)

@rt('/newfriend/{id}/update')
def post(id: int, name: str, experience: int, cv: str, tags: list[str]):
    """
    Post route for updating friend
    """
    friend = Person.get_by_id(id)
    friend.name=name 
    friend.experience=experience 
    friend.cv_location=cv
    friend.save()

    skills = SkillTag.select().where(SkillTag.id.in_(tags))
    
    PersonSkill.delete().where(PersonSkill.person == friend).execute()

    for skill in skills:
        PersonSkill.create(person=friend, skill=skill)
    
    return Redirect("/")

##############################################################################
def get_jobs_div():
    positions = (Position
                 .select(Position, PositionSkill, SkillTag)
                 .join(PositionSkill)
                 .join(SkillTag))
    print(positions)
    pos_dict = {
        pos.id: {
            'cname': pos.company,
            'jname': pos.position_name,
            'job_link': pos.job_link,
            'skills': [
                sk.skill.name for sk in pos.skills
            ],
            'experience': pos.experience
        }
        for pos in positions
    }

    print(pos_dict)
    return Div(
        H2("Job Openings", cls="text-2xl font-semibold text-gray-800 mb-4"),
        *[
            Div(
                Div(
                    Span(f"{v['jname']} at {v['cname']}",
                         cls="font-medium text-gray-700"),
                    Span(f"Skills: " +
                         ', '.join(v['skills']),
                         cls="text-sm text-gray-500"),
                    Span(f"Experience: {v['experience']} years",
                         cls="text-sm text-gray-500"),
                    cls="flex space-x-4"
                ),
                Div(
                    Span("Job Link: ", cls="font-medium text-gray-700"),
                    A(f"{v['job_link']}", href=f"{v['job_link']}", 
                      cls="text-blue-600 hover:text-blue-800")
                ),
                Div(
                    A("Edit", href=f"/newjob/{k}/edit", cls="text-blue-600 hover:text-blue-800"),
                    A("Delete", href="#", cls="text-red-600 hover:text-red-800"),
                    cls="space-x-2"
                ),
                cls="flex justify-between flex-col mb-4",  # items-center
                id=f"{k}"
            )
            for k,v in pos_dict.items()
        ],
        Div(
            A(
                " + Add Job ",
                href="/newjob",
                cls="text-green-600 hover:text-green-800"
            ),
            cls=""
        ),
        cls="bg-white p-6 rounded-lg shadow-md mb-6  max-h-96 overflow-y-scroll"
    )

def o_get_newjob(cname = '', jname = '', job_link='', experience = '',
                 tags = [], id = None):
    skills = [skl for skl in SkillTag.select().order_by(fn.Lower(SkillTag.name))]
    return position_form(id = id, company_name=cname, job_name=jname,
                         job_link=job_link, experience=experience,  skills=[{
                             'name': skl.name, 
                             'id': skl.id,
                             'selected': skl.id in tags
                             } for skl in skills])


@rt('/newjob')
def get():
    """
    Render form for adding new job
    """
    return o_get_newjob()

@rt('/newjob')
def post(cname: str, jname: str, jlink: str, experience: int, tags: list[str]):
    """
    Post route for adding new job
    """
    print(f'{cname=} {jname=} {experience=} {tags=}')
    print()
    position = Position(company = cname, position_name = jname,
                        job_link = jlink,
                        experience = experience)
    position.save()

    skills = SkillTag.select().where(SkillTag.id.in_(tags))
    for skill in skills:
        print(skill.id, skill.name)

    for skill in skills:
        PositionSkill(position=position, skill=skill).save()

    return Redirect("/")

@rt('/newjob/{id}/update')
def post(id: int, cname: str, jname: str, jlink: str, experience: int, 
         tags: list[str]):
    """
    Post route for updating job
    """
    pos = Position.get_by_id(id)
    pos.company = cname
    pos.position_name = jname
    pos.job_link = jlink
    pos.experience = experience
    pos.save()

    skills = SkillTag.select().where(SkillTag.id.in_(tags))
    
    PositionSkill.delete().where(PositionSkill.position == pos).execute()

    for skill in skills:
        PositionSkill.create(position=pos, skill=skill)

    return Redirect("/")


@rt('/newjob/{id}/edit')
def get(id: int):
    """
    Get edit form for job
    """
    pos = Position.get_by_id(id)
    skills = PositionSkill.select().where(PositionSkill.position == id)
    
    return o_get_newjob(pos.company, pos.position_name, pos.job_link,
                        pos.experience,
                           [sk.skill.id for sk in skills], id)

##############################################################################
def get_skill_dev():
    # get skills sorted by name, case insensitive    
    skills = [sk.name for sk in SkillTag.select().order_by(fn.Lower(SkillTag.name))]

    return Div(
        H2("Skills", cls="text-2xl font-semibold text-gray-800 mb-4"),
        *[Div(
            Div(
                Span(f"{sk}", cls="font-medium text-gray-700"),
                Span("Tag", cls="text-sm text-gray-500"),
                cls="flex space-x-4"
            ),
            Div(
                A("Edit", href="#", cls="text-blue-600 hover:text-blue-800"),
                A("Delete", href="#", cls="text-red-600 hover:text-red-800"),
                cls="space-x-2"
            ),
            cls="flex flex-col justify-between mb-4"  # items-center
        ) for sk in skills],
        # Div(
        #     Div(
        #         Span("React", cls="font-medium text-gray-700"),
        #         Span("Tag", cls="text-sm text-gray-500"),
        #         cls="flex space-x-4"
        #     ),
        #     Div(
        #         A("Edit", href="#", cls="text-blue-600 hover:text-blue-800"),
        #         A("Delete", href="#", cls="text-red-600 hover:text-red-800"),
        #         cls="space-x-2"
        #     ),
        #     cls="flex flex-col justify-between mb-4"  # items-center
        # ),
        Div(
            A(
                " + Add Skill ",
                href="/newskill",
                cls="text-green-600 hover:text-green-800"
            ),
            cls=""
        ),
        cls="bg-white p-6 rounded-lg shadow-md mb-6 max-h-96 overflow-y-scroll"
    )

@rt('/newskill')
def get():
    return Div(
        A(
            "Home",
            href="/",
            cls="text-xl text-blue-500 mb-3"
        ),
        H1(
            "Add New Skill",
            cls="text-3xl font-bold text-gray-800 mb-3",
        ),
        Div(

            Form(
                Div(
                    Label(
                        "Skill Name",
                        for_="name",
                        cls="block text-gray-700 font-medium mb-2",
                    ),
                    Input(
                        type="text",
                        id="name",
                        name="name",
                        cls="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                        required=True
                    ),
                    cls="mb-4",
                ),
                Div(
                    Button(
                        "Add Skill",
                        type="submit",
                        cls="w-full py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 " \
                            "focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    cls="mt-4",
                ),
                action="#",
                method="POST",

            ),
            cls="bg-white p-6 rounded-lg shadow-md",
        ),
        cls="max-w-xl mx-auto p-6 mt-4 mb-12"
    )

@rt('/newskill')
def post(name: str):
    SkillTag(name=name).save()
    return Redirect("/")


serve()

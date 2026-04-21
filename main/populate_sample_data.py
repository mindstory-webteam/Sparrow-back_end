"""
Sample data script for Journey Milestones and Team Members
Run this in Django shell: python manage.py shell
Then copy and paste this code
"""

from main import JourneyMilestone, TeamMember

# Create Journey Milestones
milestones_data = [
    {
        'year': 2017,
        'label': 'The Beginning',
        'title': '2017',
        'description': 'Incorporated in a remote area of Kerala with the vision of expanding its network throughout the entire state in automotive spare parts industry.',
        'order': 1
    },
    {
        'year': 2018,
        'label': 'First Operations',
        'title': '2018',
        'description': 'With just three employees, the company started operations focusing on the two nearest districts and achieved a sustainable turnover.',
        'order': 2
    },
    {
        'year': 2020,
        'label': 'Expansion Phase',
        'title': '2020',
        'description': "The company's employee base grew to 15 as it expanded its network to five districts and saw a significant rise in sales.",
        'order': 3
    },
    {
        'year': 2022,
        'label': 'Digital Transformation',
        'title': '2022',
        'description': 'To support growing sales and logistics operations across five districts, the company implemented SAP Business One and also added an additional warehouse.',
        'order': 4
    },
    {
        'year': 2023,
        'label': 'Continued Success',
        'title': '2023',
        'description': 'Celebrating continued success by expanding the network to 10 districts, adding another warehouse, and growing the team to 36 employees.',
        'order': 5
    },
    {
        'year': 2024,
        'label': 'Market Diversification',
        'title': '2024',
        'description': 'To meet growing customer demand, the company expanded its warehouse capacity to 5,000 sq. ft., strengthened its management team, and entered the lubricants and oils market.',
        'order': 6
    },
    {
        'year': 2025,
        'label': 'Major Milestone',
        'title': '2025',
        'description': 'As a milestone in our operational growth, we are proud to become an official distributor of Shell, a global leader in oils and lubricants.',
        'order': 7
    },
]

for milestone_data in milestones_data:
    JourneyMilestone.objects.create(**milestone_data)
    print(f"Created milestone: {milestone_data['year']}")

# Create Team Members
team_data = [
    {
        'name': 'Ginto Paul',
        'position': 'Founder & Managing Director',
        'position_type': 'founder',
        'bio': 'Visionary leader with extensive experience in the automotive industry.',
        'order': 1
    },
    {
        'name': 'Poulose E V',
        'position': 'Co-Founder & Director',
        'position_type': 'co_founder',
        'bio': 'Strategic thinker driving business growth and operational excellence.',
        'order': 2
    },
    {
        'name': 'Simi Kuriyakose',
        'position': 'Director',
        'position_type': 'director',
        'bio': 'Dedicated professional committed to organizational success.',
        'order': 3
    },
    {
        'name': 'Babu Malieckal Ouseph',
        'position': 'Director',
        'position_type': 'director',
        'bio': 'Experienced director focused on sustainable business practices.',
        'order': 4
    },
    {
        'name': 'Babu Paul K',
        'position': 'Director',
        'position_type': 'director',
        'bio': 'Results-oriented leader with a passion for innovation.',
        'order': 5
    },
    {
        'name': 'Ajil Samuel',
        'position': 'Director',
        'position_type': 'director',
        'bio': 'Strategic advisor with deep industry knowledge.',
        'order': 6
    },
]

for member_data in team_data:
    TeamMember.objects.create(**member_data)
    print(f"Created team member: {member_data['name']}")

print("\n✅ Sample data created successfully!")
print("You can now view the data in Django admin or on your about page.")
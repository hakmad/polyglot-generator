from setuptools import setup, find_packages


setup(
        name="polyglot_generator",
        packages=find_packages(exclude=["test"]),
        entry_points={
            "console_scripts": [
                "polyglot_generator=polyglot_generator.main:main"
            ],
        },
)

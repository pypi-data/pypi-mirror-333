from setuptools import setup, find_packages

setup(
    name="eshaansmart",  # Name of your game
    version="2.0.0",  # Starting version
    description="A clone of the Monkey Mart game where players pick and sell fruits to earn money.",
    author="Eshaan Buddhisagar",  # Your name
    author_email="your.email@example.com",  # Replace with your email
    url="https://github.com/yourusername/EshaansMart",  # Replace with your GitHub project URL
    packages=find_packages(),
    install_requires=[  # Add any dependencies your game might need, e.g., pygame, pyglet, etc.
        'pygame>=2.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust license if needed
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

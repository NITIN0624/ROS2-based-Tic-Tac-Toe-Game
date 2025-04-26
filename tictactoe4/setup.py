from setuptools import setup

package_name = 'tictactoe4'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yourname',
    maintainer_email='you@example.com',
    description='Tic Tac Toe game against AI with 3 difficulty levels',
    entry_points={
        'console_scripts': [
            'play = tictactoe4.game_node:main',
        ],
    },
)


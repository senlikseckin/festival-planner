AI-Powered Music Festival Planner
=================================

Welcome to the AI-Powered Music Festival Planner! This project leverages the AutoGen framework to create a team of AI agents that assist in planning a music festival. The goal is to optimize band selection to maximize audience turnout while staying within budget and ensuring compatibility among bands.

This is a proof-of-concept (POC) project designed to demonstrate how AI agent teams can streamline and accelerate the decision-making process. By enabling decision-makers to directly interact with an optimization engine, they can pose "what if" scenarios directly to a team of AI agents and receive immediate answers. This approach eliminates the need for involving experts such as planners, analysts, and engineers, thereby making decisions faster and more efficient

# Introduction

Planning a music festival involves numerous challenges, such as budget constraints, band compatibility, and audience appeal. This project demonstrates how AI agents can collaborate to simplify decision-making processes, providing festival planners with optimal solutions quickly and efficiently.

# Demo

[![YouTube](http://i.ytimg.com/vi/RfYTR5lovBA/hqdefault.jpg)](https://www.youtube.com/watch?v=RfYTR5lovBA)

https://www.youtube.com/watch?v=RfYTR5lovBA&ab_channel=SeckinSenlik


# Features

AI Team Collaboration: Multiple AI agents work together to find the best band lineup.
Budget Management: Ensures the selected bands fit within the given budget.
Compatibility Check: Evaluates band compatibility to avoid conflicts and ensure a harmonious event.
Audience Maximization: Aims to attract the largest possible audience.
Scenario Analysis: Allows users to test different "what if" scenarios to see how changes affect the outcome.

# Installation

To get started with the AI-Powered Music Festival Planner, follow these steps:

1. git clone https://github.com/senlikseckin/festival-planner.git
2. cd festival-planner
3. pip install -r requirements.txt
4. Enter your personal OpenAPI key in app.py

# Usage

To launch the user interface through the terminal and start chatting with the AI Agents, use the following command:
``` sh
    $ panel serve app.py
```
You can always modify the input parameters in work_dir/festival_planning.xlsx.

# Usefull resources:

I used three key resources for implementing this app; you can review them for more information.

1. Microsoft's Autogen examples for how to use its features:
https://microsoft.github.io/autogen/docs/Examples

2. Microsoft's OptiGuide on GitHub for adding a language model to the optimizer:
https://github.com/microsoft/optiguide

3. A YouTube tutorial by Yeyu Lab on creating the user interface using Panel:
https://www.youtube.com/watch?v=mFmPDyLlj1E&t=225s&ab_channel=YeyuLab
# Expense-Tracker
Track and manage expenses using efficient tables and visualizations

# Introduction:

The Expense Tracker application is designed to help users efficiently track their expenses and manage their finances. It provides a user-friendly interface to input, categorize, and view expenses, as well as analyze spending trends over time. The application allows users to add new expenses, view expenses by category, and visualize their financial trends through graphs and charts.

# Problem Domain:

In today's fast-paced world, managing personal finances can be challenging. Many people struggle with tracking their daily expenses and understanding where their money is going. This application aims to solve that problem by providing an easy-to-use tool for individuals to record their expenses, categorize them, and gain insights into their financial behavior. The application can be particularly useful for people looking to stick to a budget or gain better control over their spending.

# Expected Outcome and Solution:

The primary goal of the Expense Tracker is to help users:
1.	Add Expenses: Users can add new expenses with details such as date, amount, category, and description.
2.	View Expenses by Category: Expenses are grouped by categories such as housing, transportation, food, etc., providing a clear breakdown of where money is being spent.
3.	Analyze Spending Trends: The application generates visualizations, such as pie charts and line graphs, to help users understand their spending patterns over time.
4.	Track Monthly and Weekly Trends: Users can view their spending habits for different periods (last 7 days, monthly summaries) to monitor their financial health and identify trends.
The solution is built using Flask as the web framework, SQLite for data storage, and Chart.js for data visualization.

# Requirements:

# Data Structure:

Below is a list of the most relevant DSA concepts used in this project:
1. Arrays/Lists: The list is used extensively to hold data such as the list of expenses, categories, or dates. Expenses, categories, and trends are stored in lists to group data, iterate over, and present it in tables or charts.
2. Dictionaries: Data like total expense per month or per category is efficiently stored in dictionaries, where the keys represent the months or categories, and the values store the aggregated totals. 
3. Hashing: Dictionaries in Python are implemented using hashing, enabling quick lookups of total expenses per category or per month. This ensures that when you aggregate or retrieve data (like total expenses per category), the operations are done in constant time.
4. Sorting: Expenses are sorted based on dates, either by month or by individual entries, to ensure the data is presented in the correct order (chronologically).
5. Sliding Window Algorithm: The sliding window algorithm is used to calculate trends over a period (e.g., the last 7 days). 

# Software Required:

1.	Flask: The web framework for building the application.
2.	SQLite: A lightweight database for storing expenses data.
3.	Chart.js: A JavaScript library used for creating charts to visualize spending trends.
4.	HTML/CSS: For the user interface and styling.
5.	JavaScript: For interactive elements, such as the dynamic category dropdown and chart rendering.
6.	Bootstrap: For responsive layout and design.

# Methodology

# 1.	Backend:
- The application is built using Flask, which serves as the backend server.
-	SQLite is used to store user expenses, which are stored in an expenses table.
-	Various helper functions are defined to retrieve, aggregate, and display data, such as calculating monthly totals and spending trends.
# 2.	Frontend:
-	The user interface is built using HTML and CSS, following a responsive design using Bootstrap.
-	The application dynamically updates data on the frontend using Flask templates to display grouped expenses, charts, and trends.
-	JavaScript is used to handle dynamic updates like adding custom categories and generating charts with Chart.js.
# 3.	Key Features:
-	Add Expense: A form to input expense data (date, amount, category, description).
-	Category Breakdown: A page that shows the total amount spent in each category, along with a pie chart visualization.
-	Spending Trends: A page that displays spending patterns over the last 7 days using a line chart.
   Expense Overview: Displays a table with all expenses and their details.
 	
Home page view:
![image](https://github.com/user-attachments/assets/8e098def-dd92-4300-b0eb-beb4819275ce)

Add Expense view:
![image](https://github.com/user-attachments/assets/cc091f21-c32c-4866-abcb-5c08c788f059)

Category Breakdown view:
![image](https://github.com/user-attachments/assets/fa11b1e3-b9f3-4285-b1b2-429480de4b1b)

Spending Trends view:
![image](https://github.com/user-attachments/assets/c728bdd0-75f1-4645-9022-1172177c008e)


# Conclusion

The Expense Tracker is an easy-to-use tool that empowers individuals to monitor their expenses, understand their financial habits, and make informed decisions. By visualizing trends and providing detailed breakdowns, this application allows users to stay on top of their budget and control their spending. The combination of a simple user interface, powerful backend features, and data visualization tools makes the Expense Tracker an effective solution for personal financial management.

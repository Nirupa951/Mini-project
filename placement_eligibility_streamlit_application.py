import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
st.title("STREAMLIT APPLICATION")
conn = sqlite3.connect(r"C:\Users\DELL\Desktop\nirupa\Guvi\placement_eligible.db")
cursor=conn.cursor()
st.title("placement eligibility filter")
st.markdown("""Filter to find eligible students in placement criteria""")
st.sidebar.header("Filter criteria")
min_problems_solved=st.sidebar.slider("problems solved",0,100,50)
soft_skills_score=st.sidebar.slider("soft_skills_score",0,100,75)
sql_query=f""" SELECT s.student_id,s.name,s.age,s.email,s.phone,s.city,p.language,p.problems_solved,ss.communication,ss.teamwork,ss.presentation,ss.leadership,ss.critical_thinking,ss.interpersonal_skills
From students s
INNER JOIN programming_table p ON s.student_id=p.student_id
INNER JOIN soft_skills_table ss ON s.student_id=ss.student_id
WHERE p.problems_solved>={min_problems_solved} AND
(ss.communication+ss.teamwork+ss.presentation+ss.leadership+ss.critical_thinking+ss.interpersonal_skills)/6>{soft_skills_score}"""
df=pd.read_sql_query(sql_query,conn)
st.write(min_problems_solved)
st.write(soft_skills_score)
st.metric("eligible students",len(df))
st.subheader("students eligible")
st.dataframe(df)
st.download_button("⬇️ Download CSV", df.to_csv(index=False), "eligible_students.csv", "text/csv")

#SQL QUERIES
tab1, tab2, tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10 = st.tabs([" Weak Soft Skills", " Students per City", " Top 5 Placement Ready","students with problem solved","old student","students by programming language","students aged between 20 to 24","python programmers","total no.of members placed","highest package offered"])

# Tab 1: Weak Soft Skills (< 60)
with tab1:
    st.subheader("Students with Weak Soft Skills (Avg < 60)")
    weak_query = """
    SELECT 
        s.name,
        s.email,
        ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + 
               ss.critical_thinking + ss.interpersonal_skills)/6.0, 2) AS soft_avg
    FROM students s
    JOIN soft_skills_table ss ON s.student_id = ss.student_id
    WHERE (ss.communication + ss.teamwork + ss.presentation + ss.leadership + 
           ss.critical_thinking + ss.interpersonal_skills)/6.0 < 60
    """
    weak_df = pd.read_sql_query(weak_query, conn)
    st.dataframe(weak_df)

# Tab 2: Students per City
with tab2:
    st.subheader("Number of Students per City")
    city_query = """
    SELECT city, COUNT(*) AS student_count
    FROM students
    GROUP BY city
    ORDER BY student_count DESC
    """
    city_df = pd.read_sql_query(city_query, conn)
    st.dataframe(city_df)
    st.bar_chart(city_df.set_index("city"))

# Tab 3: Top 5 Placement Ready Students
with tab3:
    st.subheader(" Top 5 Placement-Ready Students")
    top5_query = """
    SELECT 
        s.name,
        s.email,
        p.problems_solved,
        ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + 
               ss.critical_thinking + ss.interpersonal_skills)/6.0, 2) AS soft_skills_avg
    FROM students s
    JOIN programming_table p ON s.student_id = p.student_id
    JOIN soft_skills_table ss ON s.student_id = ss.student_id
    ORDER BY p.problems_solved DESC, soft_skills_avg DESC
    LIMIT 5
    """
    top5_df = pd.read_sql_query(top5_query, conn)
    st.dataframe(top5_df)
with tab4:
    st.subheader("students with problem solved <30")
    df4=pd.read_sql_query("""
    SELECT s.name, p.problems_solved
    FROM students s
    JOIN programming_table p ON s.student_id = p.student_id
    WHERE p.problems_solved < 300""",conn)
    st.dataframe(df4)
with tab5:
    st.subheader("max age of student ")
    df5 = pd.read_sql_query("SELECT name, age FROM students ORDER BY age DESC LIMIT 1", conn)
    st.metric("Oldest Student", df5['name'][0], f"Age: {int(df['age'][0])}")

with tab6:
    st.subheader("Students by Programming Language")
    df6 = pd.read_sql_query("""
        SELECT language, COUNT(*) as count FROM programming_table GROUP BY language
    """, conn)
    st.dataframe(df6)

with tab7:
    st.subheader("Students Aged 20-23")
    df7 = pd.read_sql_query("""
        SELECT * FROM students WHERE age BETWEEN 20 AND 23
    """, conn)
    st.dataframe(df7)
with tab8:
    st.subheader("python programmers")
    df8=pd.read_sql_query("""
    SELECT s.name,p.language 
    FROM students s JOIN programming_table p ON s.student_id=p.student_id
    WHERE p.language="python" """,conn)
    st.dataframe(df8)
with tab9:
    st.subheader("total no.of numbers placed")
    df9=pd.read_sql_query("""
    SELECT COUNT(*) AS total_placed
    FROM placement_table
    WHERE LOWER(placement_status) = 'placed' """,conn)
    total_placed = int(df9['total_placed'][0])
    st.metric(" Total Placed Students", total_placed)
with tab10:
    st.subheader("highest package offered")
    df10=pd.read_sql_query("""
    SELECT MAX(placement_package) as highest_package
    FROM placement_table""",conn)
    highest=(df10['highest_package'][0])
    st.metric("highest_package",highest)



conn.close()
from fastapi import FastAPI
import streamlit as st
import requests
import pandas as pd
from app.database import database

st.set_page_config(layout="wide")

app = FastAPI()

database()


def main():
    def read_posts():
        url = "http://127.0.0.1:8000/tables"
        response = requests.get(url)
        table = response.json()
        df = pd.DataFrame(table)
        st.dataframe(df, use_container_width=True)

    def submit_post():
        url = "http://127.0.0.1:8000/tables"
        payload = details
        requests.post(url, json=payload)

    def read_post():
        url = f"http://127.0.0.1:8000/tables/{id}"
        response = requests.get(url)
        data = response.json()
        return data

    def update_post():
        url = f"http://127.0.0.1:8000/tables/{id}"
        payload = details
        requests.put(url, json=payload)

    def delete_post():
        url = f"http://127.0.0.1:8000/tables/{id}"
        requests.delete(url)

    def delete_check_id():
        url = f"http://127.0.0.1:8000/tables/{id}"
        response = requests.get(url)
        return response.status_code

    st.title("Nike DCU Table Onboarding Form")

    option = st.sidebar.selectbox("Select an Operation", ("Add Tables", "Read Tables", "Update Table", "Delete Table"))
    if option == "Add Tables":
        st.subheader("Update Table Details")
        with st.form("form"):
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)

            table_name = c1.text_input("Table Name", value="")
            table_key = c2.text_input("Table Key", value="")
            delete_key = c3.text_input("Delete Key", value="")
            partitioned_by = c4.text_input("Partitioned By", value="")
            dependency_dag = st.text_input("Dependency DAG", value="")
            delta_table = st.selectbox("Delta Table", ('False', 'True'))

            submitted = st.form_submit_button("Submit")

            if submitted:
                if len(table_name) <= 0 or len(table_key) <= 0 or len(delete_key) <= 0 or len(partitioned_by) <= 0:
                    st.error("Input fields cannot be empty")
                else:
                    st.success("Form Submitted Successfully")
                    details = {
                        "table_name": table_name,
                        "table_key": table_key,
                        "delete_key": delete_key,
                        "partitioned_by": partitioned_by,
                        "dependency_dag": dependency_dag,
                        "delta_table": delta_table
                    }

                    submit_post()
                    read_posts()

    elif option == "Read Tables":
        st.subheader("Read Tables")
        read_posts()

    elif option == "Update Table":
        st.subheader("Update Table Record")
        id = st.number_input("Enter ID", min_value=1)
        try:
            user_post = read_post()

            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)

            table_name = c1.text_input("Table Name", value=user_post["table_name"])
            table_key = c2.text_input("Table Key", value=user_post["table_key"])
            delete_key = c3.text_input("Delete Key", value=user_post["delete_key"])
            partitioned_by = c4.text_input("Partitioned By", value=user_post["partitioned_by"])
            dependency_dag = st.text_input("Dependency DAG", value=user_post["dependency_dag"])
            delta_table = st.selectbox("Delta Table", ("False", "True"), index=user_post["delta_table"])

            if st.button("Update"):
                details = {
                    "id": id,
                    "table_name": table_name,
                    "table_key": table_key,
                    "delete_key": delete_key,
                    "partitioned_by": partitioned_by,
                    "dependency_dag": dependency_dag,
                    "delta_table": delta_table
                }

                update_post()
                st.success("Table record Updated Successfully!!!")

            read_posts()

        except KeyError as e:
            st.error("ID not available in database. Please enter a valid ID")

    elif option == "Delete Table":
        st.subheader("Delete a Record")
        id = st.text_input("Enter ID", value="")

        if st.button("Delete"):
            delete_id = delete_check_id()
            if delete_id == 404:
                st.error("ID not available in database. Please enter a valid ID")
            else:
                delete_post()
                st.success("Table record deleted successfully!!!")
        read_posts()

    else:
        pass


if __name__ == "__main__":
    main()

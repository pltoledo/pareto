import streamlit as st
import src.pareto_front 
import pages.genetic_page

PAGES = {
    "Genetic Algorithm": pages.genetic_page,
    "2-D Pareto Front": src.pareto_front
}


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    page.write()

    st.sidebar.title("About")
    st.sidebar.info(
            """
            This app is a project made for learning simutaneously about Streamlit and multi-objective optmization algorithms. 
            It is maintained by Pedro Toledo, statistics undergraduate and Data Scientist.
        """
        )


if __name__ == "__main__":
    main()
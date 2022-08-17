import json
import requests
from datetime import datetime
import streamlit as st

# --------website----------

st.set_page_config(
    page_title="The American Museum",
    layout="wide"
)

st.markdown("# The American Museum")
st.markdown("#### The curator is called upon to select a topic for today's exhibit: ")

# button
search_term = ""

def update_search():
    st.session_state.k_search = st.session_state.k_search
    search_term = st.session_state.k_search

search_term = st.text_input(
    label = "Exhibition Focus:",
    value = "",
    placeholder = "limestone, e.g.")

# --------code ------

def curate():
    st.markdown("##### The so-called '" + search_term + "' has had a long and complicated life in the history of this country. Let's take a look at some of its moments, large and small.")
    st.write("Curation may take a moment, please be patient. These things take time ... ")
    st.markdown("""---""")

    # build the api query
    response_API = requests.get(
        "https://catalog.archives.gov/api/v1/?rows=35&q="
        + search_term
        + "&resultTypes=item&description.item.generalRecordsTypeArray.generalRecordsType.termName=%22Photographs%20and%20other%20Graphic%20Materials%22")

    # load and parse the json object
    q = response_API.text
    parsed_query = json.loads(q)
    results = parsed_query["opaResponse"]["results"]["result"]

    image_records = []

    for result in results:
        url = ""
        title = ""
        caption = ""
        date = ""

        # getting the image url
        try:
            url = result["objects"]["object"]["file"]["@url"]
        except:
            pass

        if (url != ""):
            # extra info, not necessary
            try:
                title = result["description"]["item"]["title"]
            except:
                pass

            try:
                caption = result["description"]["item"]["scopeAndContentNote"]
            except:
                pass

            try:
                date = result["description"]["item"]["productionDateArray"]["proposableQualifiableDate"]["logicalDate"]
                date = date[:10]
                d_obj = datetime.strptime(date, '%Y-%m-%d')
                date = d_obj.strftime("%B") + " " + d_obj.strftime("%d") + ", " + d_obj.strftime("%Y")
            except:
                pass

            image_records.append([url, title, caption, date])


    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col3:
        st.write("")

    # drawing the data onto the page
    n_records = len(image_records)

    if(n_records > 5):
        for x in range(1,6):
            # choose an image from the dictionary
            image_step = n_records / 5
            index = int((image_step * x) - 1)

            # in the center column
            with col2:
                st.markdown(
                    "<img src='" + image_records[index][0] + "' alt='Exhibit' width='100%'/>",
                    unsafe_allow_html=True)

                # print extra information
                st.markdown("")
                st.markdown(image_records[index][3])
                st.markdown("###### *" + image_records[index][1] + "*")
                # st.markdown(image_records[index][2])
                st.markdown("""---""")

    else:
        if (not image_records):
            st.write("There are no pictures of that being in America.")
        else:
            for img in image_records:
                st.markdown(
                    "<img src='" + img[0] + "' alt='Exhibit' width='710'/>",
                    unsafe_allow_html=True)
                # print extra information
                st.markdown("")
                st.markdown(img[3])
                st.markdown("*" + img[1] + "*")
                #st.markdown(img[2])
                st.markdown("""---""")

if st.button('Curate'):
    curate()

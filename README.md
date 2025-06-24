# *Anonymous Graffiti & Street Art Database*

## A graffiti and street art database focused on anonymity.  

![GRAFF DB]("assets/GRAFF DB - SCALED - NO BG (1).png")

### I've always had a keen interest in both graffiti and computers. When I was getting into graffiti, I found it difficult to find a centralized database for inspiration or to quickly check if certain names or styles were overused. This personal challenge was the driving force behind creating this platform – an anonymous space for the community to share and explore street art. Around them and in the whole world!

#### I have been actively developing this project since early January 2025. This entire endeavor has been an incredibly insightful journey, truly guiding me through learning a multitude of modern development concepts and practices. Building this application from the ground up served as a practical bootcamp, pushing me to understand how different components integrate to deliver a functional and interactive platform. Teaching me better than any tutorial.

#### Key Technologies & Learning Journey:

This project is built predominantly with **Python** and features a dynamic web-based interface crafted using **Streamlit**. Creating the interactive elements and structuring the application within the Streamlit framework was a significant learning curve, greatly enhancing my web application development skills.

For the crucial interactive map functionality, `streamlit-folium` was utilized, seamlessly integrating **Folium** maps. This process was fascinating, as I delved into how Folium leverages underlying technologies like `Leaflet.js` and `OpenStreetMap` data to render engaging geographical visualizations. It taught me a lot about spatial data and web mapping.

On the backend, a robust data management system was implemented using **SQLite3**. This hands-on experience was fundamental, guiding me through the intricacies of database design, persistence, and, most importantly, mastering various **SQL requests**. I gained practical proficiency in performing everything from basic data insertions to more complex queries to retrieve and manage information effectively.

Beyond the main components, this project really deepened my understanding of **API interactions and web requests**. It's where I truly grasped how applications communicate with and grab live data from outside services. I jumped right into Python's powerful `requests` library, figuring out how to send specific **GET requests** for things like precise geocoding (for example the Nominatim API was super handy!). I also got to grips with handling important **HTTP headers** (gotta be a good netizen, right?) and how to manage those tricky network errors. Turning raw **JSON data** into something usable for my app quickly became second nature.

My journey also pushed me to understand foundational web styling. I got to play around with **HTML** and **CSS**, directly tweaking how things look in Streamlit using `st.markdown` to fine-tune the user interface's aesthetics. Plus, handling local data storage, image uploads, and just navigating the file system was a major learning curve, thanks to Python's built-in **`os` module**. That taught me critical skills for dynamic path management and directory operations – super important for any solid application. What was truly exciting was diving into the **`socket` module**! That unlocked the nuts and bolts of network communication. I got hands-on with lower-level **TCP/IP connections**, figuring out client-server handshakes, and how to send structured data using **JSON** to make things flow smoothly. This whole hands-on experience, from getting my app to talk to the wider internet to mastering its local environment, was incredibly rewarding. It showed me just how much more I can build!

Thanks to all the contributors behind these amazing open-source tools and libraries! &nbsp;&nbsp;❤

### Author: Roadbobek

## Requirements

* Python 3.13:
    * **Streamlit:** (Python package) Install via pip: `pip install streamlit`
    * **Folium:** (Python package) Install via pip: `pip install folium`
    * **streamlit-folium:** (Python package) Install via pip: `pip install streamlit-folium`

## License

#### Copyright (c) 2025 Roadbobek

This software is licensed under the MIT License. <br>
See the LICENSE.txt file for details

#### MIT License
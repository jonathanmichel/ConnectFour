FROM python:3.7

# Add Linux user
#RUN adduser -D connectfour

# Set default directory in previously created profile
WORKDIR /home/lucblender/ConnectFour/server

# Install python requirements in virtual environment
COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install libcairo2-dev
RUN pip install -r requirements.txt

# Copy applications files
ADD ConnectFour /home/lucblender/ConnectFour

# FLASK_APP environment variable is required by flask
ENV FLASK_APP flask_four_in_a_row.py

# Ensure all files in work directory are owned by connectfour
#RUN chown -R connectfour:connectfour ./

# Make connectfour user the default for any subsequent instructions
# And also for when the container is started
#USER connectfour

# Define server port to use
EXPOSE 5002

RUN ls /home/lucblender/ConnectFour/server

# Define command to execute when container is started
ENTRYPOINT ["python3", "flask_four_in_a_row.py"]

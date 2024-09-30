FROM python:3.10.12
ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"
COPY ./requirements.txt
RUN pip install -r ./requirements.txt
COPY . .



# Настроить и активировать виртуальную среду
# ENV VIRTUAL_ENV "/venv"
# RUN python -m venv $VIRTUAL_ENV
# ENV PATH "$VIRTUAL_ENV/bin:$PATH"
 
# Команды Python будут выполнены в виртуальной среде
# RUN python -m pip install \
#        parse \
#        realpython-reader

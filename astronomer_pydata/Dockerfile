FROM astronomerinc/ap-airflow:0.10.1-alpha.15-1.10.5-onbuild
COPY nb_originals /nb_originals
COPY datasets /datasets
RUN chmod 777 -R /datasets

RUN mkdir /nb_outputs && chmod 777 /nb_outputs
python compile.py build_ext --inplace
python compile.py clean --all
mv ./*.so ./src/
cd ./src/ \
    && rm *.py \
    && rm *.c

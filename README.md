# showcase_mtls_sample

## Download the repo.
```
git clone https://github.com/arithmetic1728/showcase_mtls_sample.git
```

Go to the repo directory.
```
cd showcase_mtls_sample
```

Create virtualenv.
```
pyenv virtualenv showcase_mtls_sample
pyenv local showcase_mtls_sample
```

Install dependencies.
```
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Get the showcase server.
Download showcase server.
```
go get https://github.com/arithmetic1728/gapic-showcase
```

Build the server.
```
cd $GOPATH/src/github.com/arithmetic1728/gapic-showcase/cmd/gapic-showcase
go build
```

Provide cert/key for mTLS and run the server.
```
./gapic-showcase run --mtls-ca-cert=<showcase_mtls_sample_path>/server.crt \
--mtls-cert=<showcase_mtls_sample_path>/server.crt \
--mtls-key=<showcase_mtls_sample_path>/server.key
```

## Run the test.
```
cd <showcase_mtls_sample_path>
python -m pytest sample_test.py
```

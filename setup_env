#/usr/bin/sh
# Prerequisite Ubuntu 16.04

print_help()
{
    echo "To setup environment"
    echo "$ ./setup_env setup_env"
    echo "To run locally:"
    echo "$ ./setup_env run_local"
}

setup_env() 
{
    # Setup NPM
    sudo apt-get install npm
    cd Web; npm install; cd ..

    # Python virtualenv
    [ -d ./env ] | virtualenv --python=python3 env
    . env/bin/activate
    pip install -r requirements.txt

    echo Now activate the Python virtual environment with
    echo source env/bin/activate
}

run_local() {
    cd Web; npm build; cd ..
    python run_flask.py
}

case $1 in
    setup_env)
        setup_env ;;
    run_local) 
        run_local ;;
    *)
        print_help ;;
esac

#!/bin/sh
# Prerequisite: Ubuntu 18.04

DEFAULT_JSPM=yarn

install_jspm()
{
    case $1 in
    yarn)
        sudo apt-get install npm
        sudo npm install -g yarn 
        ;;
    npm) 
        sudo apt-get install npm 
        ;;
    *)
        echo JSON package manager \'$1\' not supported  
        exit 1
        ;;
    esac
}

print_help()
{
    echo "To setup environment"
    echo "$ ./setup_env.sh setup_env"
    echo "To run Flask app locally:"
    echo "$ ./setup_env.sh run_local"
}

setup_env() 
{
    # Setup JS packages
    [ -x $DEFAULT_JSPM ] || install_jspm $DEFAULT_JSPM
    cd Web; $DEFAULT_JSPM install; cd ..

    # Python virtualenv
    [ -d ./env ] || virtualenv --python=python3 env
    . env/bin/activate
    pip install -r requirements.txt

    echo Now activate the Python virtual environment with
    echo source env/bin/activate
}

run_local() {
    cd Web; $DEFAULT_JSPM build; cd ..
    python run_flask.py
}

case $1 in
    setup_env)
        setup_env
        ;;
    run_local) 
        run_local
        ;;
    *)
        print_help 
        ;;
esac

make html;
if [ ! -d "Simple_Ldap_Api_gh-pages" ]; then
    git clone git@bitbucket.org:Milor123/simple_ldap_api.git 
    mv simple_ldap_api simple_ldap_api_gh-pages
    cd simple_ldap_api_gh-pages
    git branch gh-pages
    git checkout gh-pages
    cd ..
fi
cp -r $PWD/_build/html/* $PWD/simple_ldap_api_gh-pages/
cd simple_ldap_api_gh-pages
git push add .
git commit
git push origin gh-pages
cd ..
#rm -r simple_ldap_api_gh-pages

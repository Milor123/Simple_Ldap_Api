make html;
if [ ! -d "Simple_Ldap_Api_gh-pages" ]; then
    git clone git@bitbucket.org:Milor123/simple_ldap_api.git 
    mv Simple_Ldap_Api Simple_Ldap_Api_gh-pages
    cd Simple_Ldap_Api_gh-pages
    git branch gh-pages
    git checkout gh-pages
    cd ..
fi
cp -r $PWD/_build/html/* $PWD/Simple_Ldap_Api_gh-pages/
cd Simple_Ldap_Api_gh-pages
git push add .
git commit -a
git push origin gh-pages
cd ..
rm -r Simple_Ldap_Api_gh-pages

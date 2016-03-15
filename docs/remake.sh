make html;
if [ ! -d "Simple_Ldap_Api_gh-pages" ]; then
    git clone git@github.com:Milor123/Simple_Ldap_Api.git
    mv Simple_Ldap_Api Simple_Ldap_Api_gh-pages
    cd Simple_Ldap_Api_gh-pages
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

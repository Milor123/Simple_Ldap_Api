make html;
if [ ! -d "Simple_Ldap_Api_gh-pages" ]; then
    git clone git@bitbucket.org:Milor123/simple_ldap_api.git 
    mv simple_ldap_api simple_ldap_api_gh-pages
    cd simple_ldap_api_gh-pages
    git checkout gh-pages
    cd ..
fi
cp -r _build/html/* simple_ldap_api_gh-pages/
cd simple_ldap_api_gh-pages
git add .
git commit -m 'no commit'
git push origin gh-pages
cd ..
rm -r simple_ldap_api_gh-pages

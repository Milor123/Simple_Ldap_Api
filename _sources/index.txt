.. Simple_Ldap_Api documentation master file, created by
   sphinx-quickstart on Fri Mar 11 10:40:26 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simple_Ldap_Api 1.0
====================
Contents:

.. toctree::
   :maxdepth: 2
    licence.rst


.. automodule:: Appl



Requeriments
^^^^^^^^^^^^

    * ``python 2.7``
    * ``install libsasl2-dev python-dev libldap2-dev libssl-dev``
    * ``pip install python-ldap``

Documentation
=========================


.. autoclass:: Myldap
   :members:
   :private-members:
   :special-members: __init__

.. automodule:: functions.decorators
   :members:

.. automodule:: functions.convert
   :members:

.. automodule:: functions.search_this
   :members:

.. automodule:: functions.show_this
   :members:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Uso y Ejemplos (Spanish)
========================

.. |br| raw:: html

   <br />

En primera medida para hacer uso del LDAP API, se debe tener acceso a un usuario del directorio activo que poseea
los permisos y caracteristicas suficientes para llevar a cabo la labor que se desea realizar,

Autentificacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

De manera que debemos instanciar Myldap, ilustrese con el siguiente ejemplo:

>>> Nop = Myldap('192.168.0.23', 'cn=UsuarioConPermisos,cn=Users,dc=ITFIP,dc=LOCAL','mypassword')
# Aqui deberia retornarnos el usuario o un error.

o en caso querer hacer modificaciones de datos muy sensibles (contrasenas, permisos especiales, nuevos usuarios, etc.)

>>> Nop = Myldap('192.168.0.23', 'cn=UsuarioConPermisos,cn=Users,dc=ITFIP,dc=LOCAL','mypassword', ssl=True) # Habilitando el ssl
# Aqui deberia retornarnos el usuario o un error.

.. note:: Para hacer uso de esto debe conocer la estructura `DN`, lea porfavor esto https://msdn.microsoft.com/en-us/library/windows/desktop/aa366101%28v=vs.85%29.aspx

Hacer uso de alguna funcion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La mas comun de ellas es la de agregar usuario que puedan autentificarse.

Usando la Instancia `Nop` por ejemplo, ejecutamos la funcion para agregar un usuario, asi:

>>> Nop.ldapadd_user('cn=Nuevo_Usuario,cn=Users,dc=ITFIP,dc=local','Nuevo_Usuario','Contrasena_01_Compleja+')

.. note:: El usuario debe tener una contrasena compleja, y la sentencia cn=nombre debe ser igual al usuario.

|br|

Si va a  modificar informacion del usuario, un ejemplo seria:

>>> Nop.ldapmodify('cn=Nuevo_Usuario,cn=Users,dc=ITFIP,dc=local', {'telephoneNumber': '515336'})

.. note:: La sentencia **telephoneNumber** es un atributo del usuario, propio del directorio activo, que hace referencia a el numero de telefono, asi como este hay muchos atributos mas.

|br|

Podemos tambien consultar cualquier clase de dato, verificaremos si fue modificado, de la siguiente forma.

>>> Nop.ldapsearch('mail=mailfor@search.com', ['telephoneNumber']) # Ingresando manualmente los attributos
# aqui deberia retornar una sentencia de la forma ['AttributoBuscado', ['Valores_Encontrados']]] o un error

o usando las funciones agiles integrades en el API,

>>> Nop.ldapsearch(search_by_mail('mailfor@search.com'), show_telephone_number()) # Con las funciones
# aqui deberia retornar una sentencia de la forma ['AttributoBuscado', ['Valores_Encontrados']]] o un error

Ahora si queremos eliminar el usuario, seria asi:

>>> Nop.ldapdelete('cn=Nuevo_Usuario,cn=Users,dc=ITFIP,dc=local')
# Deberia retornar un mensaje diciendo que el usuario fue borrado o un error.



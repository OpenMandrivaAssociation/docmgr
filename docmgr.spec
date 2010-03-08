%define	prerel	RC6
%define	webroot	%{_var}/www/docmgr

Name:		docmgr
Version:	1.0
Release:	%mkrel 0.%{prerel}.1
License:	GPLv2
Buildarch:	noarch
Group:		System/Servers
Summary:	Web based DMS - Document Management System
URL:		http://docmgr.org/

Source0:	%{name}-%{version}%{?prerel:-%{prerel}}.tar.gz
Source1:	docmgr.init
Patch0:		docmgr-1.0-RC6-local-config.patch
Patch1:		docmgr-1.0-RC6-unified-tmpdir.patch
Patch2:		docmgr-1.0-RC6-quiet-rm.patch
Patch3:		docmgr-1.0-RC6-no-dos-eol.patch
Patch4:		docmgr-1.0-RC6-PyODConverter-1.1.patch
Patch5:		docmgr-1.0-RC6-PyODConvert-stream.patch
Patch6:		docmgr-1.0-RC6-fileconvert-ooo-profile.d.patch
Patch7:		docmgr-1.0-RC6-fix-keepalive-relative-url.patch
# As DocumentConvert.py now uses streams, we don't need to copy documents
# to a temporary directory to read them. This will also get rid of an issue
# with the input document being deleted before reading as well..
Patch8:		docmgr-1.0-RC6-dont-use-temp-copy-for-ooo-input.patch
# Use LC_TIME for date & time format if LOCALE is set
Patch9:		docmgr-1.0-RC6-locale-use-LC_TIME.patch
Patch10:	docmgr-1.0-RC6-add-mediawiki-derived-installer.patch

Requires:	mod_php php-pgsql php-iconv
Requires:	php-zip php-imap
Requires:	postgresql-server postgresql-contrib-virtual postgresql-plpgsql-virtual
Requires:	gocr ocrad imagemagick libtiff postfix file 
Requires:	xpdf xpdf-tools enscript wget zip clamav
Requires:	openoffice.org-common openoffice.org-pyuno
Requires(pre):	rpm-helper
Requires(preun):	rpm-helper

%description
DocMgr is a complete, web-based Document Management System (DMS).
It allows for the storage of any file type, and supports full-text indexing
of the most popular document formats. It is available in many different
languages and is easy to translate into new languages.

DocMgr runs on PHP, the Apache webserver, and Postgresql. It optionally
uses tsearch2 for full-text indexing which provides for faster search results
and result ranking. DocMgr supports LDAP authentication, the ability to
easily add and remove "objects" for storage in the system, document workflow,
object subscriptions, WebDAV access, and an ever-growing set of features
revolving around content storage.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .local~
%patch1 -p1 -b .tmpdir~
%patch2 -p1 -b .quiet~
%patch3 -p1 -b .dos_eol~
%patch4 -p1 -b .doc_conv1.1~
%patch5 -p1 -b .stream~
%patch6 -p1 -b .ooo~
%patch7 -p1 -b .relative~
%patch8 -p1 -b .notemp~
%patch9 -p1 -b .locale~
%patch10 -p1 -b .mw_install~
sed -e 's#postgres#docmgr#g' -i scripts/docmgr.pgsql

find -type f |xargs chmod 644

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_var}/{www,lib}/docmgr
cp -r */ *.php %{buildroot}%{webroot}
rm -rf %{buildroot}%{webroot}/{DOCS,scripts}
mv %{buildroot}%{webroot}/files %{buildroot}%{_var}/lib/%{name}

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{name}
install -m644 scripts/docmgr.pgsql -D %{buildroot}%{webroot}/scripts/docmgr.pgsql

install -d %{buildroot}%{webappconfdir}
tee %{buildroot}%{webappconfdir}/%{name}.conf << EOF
Alias /%{name} %{webroot}
<Directory "%{webroot}">
  Order allow,deny
  Allow from All
</Directory>

<Directory "%{webroot}/bin">
  Order allow,deny
  Deny from All
</Directory>
EOF

install -d %{buildroot}%{webroot}/config/{local/tmp,vendor}
tee %{buildroot}%{webroot}/config/vendor/config.php << EOF
/********************************************
  DO NOT EDIT THE SETTINGS IN THIS FILE (config/vendor/config.php)!
  Add your own local settings to config/local/config.php in stead,
  otherwise you might loose your configuration when upgrading.
********************************************/

define("DB_USER", "docmgr");
define("FILE_DIR", "%{_localstatedir}/lib/%{name}/files");
define("ADMIN_EMAIL", "root@localhost");
define("SITE_URL", "http://localhost/%{name}");
define("SITE_PATH", "%{webroot}");
define("IMPORT_DIR", IMPORT_DIR . "/import");
define("DB_CHARSET", "UTF-8");
define("VIEW_CHARSET", "UTF-8");
EOF

install -d %{buildroot}%{_sysconfdir}/sysconfig
tee %{buildroot}%{_sysconfdir}/sysconfig/%{name} << EOF
# OpenOffice.org
OOFFICE_HOST="localhost"
OOFFICE_PORT="8100"
# Any additional options to pass to ooffice can be set here
# OOFFICE_OPTIONS=""
EOF

find %{buildroot} -name \*~ |xargs rm -f

# ghost files
for conf in app-config.php config.php ldap-config.php; do
	touch %{buildroot}%{webroot}/config/local/$conf
done

%pre
%_pre_useradd %{name}

%postun
%_postun_userdel %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc DOCS/AUTHORS 
%attr(755,root,root) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config %{webappconfdir}/%{name}.conf
%dir %{webroot}
%{webroot}/apilib
%{webroot}/app
%{webroot}/auth
%{webroot}/bin
%{webroot}/ckeditor
%dir %{webroot}/config
%config %{webroot}/config/app-config.php
%config %{webroot}/config/config.php
%config %{webroot}/config/ldap-config.php
%dir %{webroot}/config/local
%dir %attr(700,apache,apache) %{webroot}/config/local/tmp
%attr(600, root, root) %config(noreplace, missingok) %ghost %{webroot}/config/local/app-config.php
%attr(600, root, root) %config(noreplace, missingok) %ghost %{webroot}/config/local/config.php
%attr(600, root, root) %config(noreplace, missingok) %ghost %{webroot}/config/local/ldap-config.php
%dir %{webroot}/config/vendor
%config %{webroot}/config/vendor/config.php
%{webroot}/config/forms
%dir %{webroot}/config/mediawiki
%{webroot}/config/mediawiki/*.php
%{webroot}/config/index.php
%{webroot}/config/*.xml
%{webroot}/controls
%{webroot}/header
%{webroot}/javascript
%{webroot}/jslib
%{webroot}/lang
%{webroot}/lib
%{webroot}/modules
%{webroot}/themes
%dir %{webroot}/scripts
%{webroot}/scripts/docmgr.pgsql
%{webroot}/api.php
%{webroot}/history.php
%{webroot}/index.php
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}/files


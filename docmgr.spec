%define	prerel	RC10
%define	webroot	%{_var}/www/docmgr

Name:		docmgr
Version:	1.0
Release:	%mkrel 0.%{prerel}.1
License:	GPLv2
Group:		System/Servers
Summary:	Web based DMS - Document Management System
URL:		http://docmgr.org/

Source0:	%{name}-%{version}%{?prerel:-%{prerel}}.tar.gz
Source1:	docmgr.init
#Patch0:		docmgr-1.0-RC10-local-config.patch
Patch1:		docmgr-1.0-RC10-unified-tmpdir.patch
Patch2:		docmgr-1.0-RC8-quiet-rm.patch
#Patch3:		docmgr-1.0-RC10-no-dos-eol.patch
Patch4:		docmgr-1.0-RC6-PyODConverter-1.1.patch
Patch5:		docmgr-1.0-RC6-PyODConvert-stream.patch
Patch6:		docmgr-1.0-RC10-fileconvert-ooo-profile.d.patch
#Patch7:		docmgr-1.0-RC6-fix-keepalive-relative-url.patch
# As DocumentConvert.py now uses streams, we don't need to copy documents
# to a temporary directory to read them. This will also get rid of an issue
# with the input document being deleted before reading as well..
# Also since we no longer create a temporary copy with an extension to detect
# the type from, we now detect it based on mime type in stead.
# NOTE: Since we lack magic for ie. OOXML files and OOo also is dependent on suffix
# to determine type, behaviour has been partly reverted to create a symlink
# in stead with the corresponding suffix...
Patch8:		docmgr-1.0-RC10-dont-use-temp-copy-for-ooo-input.patch
# Use LC_TIME for date & time format if LOCALE is set
Patch9:		docmgr-1.0-RC9-locale-use-LC_TIME.patch
#Patch10:	docmgr-1.0-RC6-add-mediawiki-derived-installer.patch
# This is mainly to avoid dependency extractor from adding dependencies on the
# conditionally included files...
#Patch11:	docmgr-1.0-RC6-conditional-include-function.patch
Patch12:	docmgr-1.0-RC6-die-if-pg_connect-fails.patch
# This will set the default timezone if defined, this to silence php warnings
# when using date() with LC_TIME.
# TODO: fetch timezone from system(?), defaults to GMT for now. Uncertain whether
# or not it's actually desired to set any other timezone, rationale for now is to
# set it only to silence php errors about it not being set when using date()..
Patch13:	docmgr-1.0-RC10-set-default-timezone.patch
# Check that user actually exists before trying to update failed_logins for it
Patch14:	docmgr-1.0-RC8-check-if-user-exists-for-failed-logins.patch
# The config file mentions RESTRICTED_DELETE, but it's not really implemented,
# so let's implement it here.
Patch15:	docmgr-1.0-RC10-restricted-delete.patch
Patch16:	docmgr-1.0-RC6-use-FILE_DIR-for-process.patch
#Patch17:	docmgr-1.0-RC6-fix-typo.patch
Patch18:	docmgr-1.0-RC6-use-correct-mime-types.patch
# Add absolute path to include_path
Patch19:	docmgr-1.0-RC10-set-include_path.patch
# Check that the OOo converter returns without error status.
# TODO: implement proper behaviour on error
Patch20:	docmgr-1.0-RC6-check-fileconvert-exit-status.patch
#Patch21:	docmgr-1.0-RC10-use-utf8-for-client_encoding.patch
Patch22:	docmgr-1.0-RC10-run-indexer-as-admin-user.patch
Patch23:	docmgr-1.0-RC8-webdav-baseUri-no-reserved-domain.patch
# Print out the actual error message within the array, rather than the
# array (type) itself. Probably not the best solution, but does at least
# provide *some* verbosity...
#Patch24:	docmgr-1.0-RC8-print-firstlogin-perm-error.patch
# Do prefix searching to allow for searching on beginning of words as you write
# them. TODO: will it work with or break postgresql < 8.4?
Patch25:	docmgr-1.0-RC8-tsearch2-prefix-search.patch
Patch26:	docmgr-1.0-RC8-update-to-ckeditor-3.2.patch
# You can only search for users in the account manager, not list them, so let's
# implement a list as well.
Patch27:	docmgr-1.0-RC9-show-user-list.patch
#Patch28:	docmgr-1.0-RC8-set-bitmask.patch
Patch29:	docmgr-1.0-RC8-check-bitset-not-bitmask.patch
Patch30:	docmgr-1.0-RC8-fix-css-themes-relative-path.patch
Patch31:	docmgr-1.0-RC9-default-perms.patch
# Split date and time in php to get it correctly with localized version
Patch32:	docmgr-1.0-RC9-split-time-and-date-in-php-not-js.patch
Patch33:	docmgr-1.0-RC9-add-missing-objectId-to-edittask-query.patch
Patch34:	docmgr-1.0-RC9-set-workflow-comment-properly.patch
Patch35:	docmgr-1.0-RC9-display-recipient-notes-for-task.patch
Patch36:	docmgr-1.0-RC9-pg_connect-accept-empty-default-values.patch
# Use host & port specified in /etc/sysconfig/docmgr if available for doc conversion
Patch37:	docmgr-1.0-RC9-docconv-host-port-sysconfig.patch
#Patch38:	docmgr-1.0-RC10-installer-use-local-config.patch
Patch39:	docmgr-1.0-RC10-make-users-directory-protected.patch
#Patch40:	docmgr-1.0-RC10-customizable-database-setup.patch
Patch41:	docmgr-1.0-RC10-enhanced-setup-and-config.patch

Requires:	mod_php mod_ssl php-pgsql php-iconv
Requires:	php-zip php-imap php-fileinfo php-mbstring
Requires:	postgresql-server >= 8.4 postgresql-contrib-virtual postgresql-plpgsql-virtual
Requires:	gocr ocrad imagemagick libtiff-progs sendmail-command
Requires:	xpdf xpdf-tools enscript wget zip clamav
Requires:	wget poppler file

BuildArch:	noarch
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
#%%patch0 -p1 -b .local~
%patch1 -p1 -b .tmpdir~
%patch2 -p1 -b .quiet~
#%%patch3 -p1 -b .dos_eol~
%patch4 -p1 -b .doc_conv1.1~
%patch5 -p1 -b .stream~
%patch6 -p1 -b .ooo~
#%%patch7 -p1 -b .relative~
%patch8 -p1 -b .notemp~
%patch9 -p1 -b .locale~
#%%patch10 -p1 -b .mw_install~
#%%patch11 -p1 -b .cond_include~
%patch12 -p1 -b .die~
%patch13 -p1 -b .timezone~
%patch14 -p1 -b .failed_logins~
%patch15 -p1 -b .restricted~
%patch16 -p1 -b .file_dir~
#%%patch17 -p1 -b .typo~
%patch18 -p1 -b .mime_types~
%patch19 -p1 -b .set_include_path~
%patch20 -p1 -b .exit_status~
#%%patch21 -p1 -b .utf8~
%patch22 -p1 -b .admin~
%patch23 -p1 -b .webdav~
#%%patch24 -p1 -b .perm_error~
%patch25 -p1 -b .prefix_search~
%patch26 -p1 -b .ckeditor3.2~
%patch27 -p1 -b .account_list~
#%%patch28 -p1 -b .bitmask~
%patch29 -p1 -b .bitset~
%patch30 -p1 -b .themes_path~
%patch31 -p1 -b .perms~
%patch32 -p1 -b .date_view~
%patch33 -p1 -b .objectId~
%patch34 -p1 -b .comment~
%patch35 -p1 -b .task_notes~
%patch36 -p1 -b .emptydefs~
%patch37 -p1 -b .hostport~
#%patch38 -p1 -b .local_installer~
%patch39 -p1 -b .protected~
#%patch40 -p1 -b .db_setup~
%patch41 -p1 -b .setup~

find -type f |xargs chmod 644

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_var}/{www,lib}/docmgr
cp -r */ *.php %{buildroot}%{webroot}
rm -rf %{buildroot}%{webroot}/{DOCS,sd}
mv %{buildroot}%{webroot}/files %{buildroot}%{_var}/lib/%{name}

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{name}

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

<IfModule mod_ssl.c>
  <LocationMatch /%{name}>
    Options FollowSymLinks
    RewriteEngine on
    RewriteCond %{SERVER_PORT} !^443$
    RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
  </LocationMatch>
</IfModule>
EOF

install -d %{buildroot}%{webroot}/config/{local/tmp,vendor}
touch %{buildroot}%{webroot}/config/local/{app-config,config}.php
tee %{buildroot}%{webroot}/config/vendor/config.php << EOF
<?php
/********************************************
  DO NOT EDIT THE SETTINGS IN THIS FILE (config/vendor/config.php)!
  Add your own local settings to config/local/config.php in stead,
  otherwise you might loose your configuration when upgrading.
********************************************/

# No host & port specified, means use postgresql defaults (unix sockets)
define("DBHOST","");
define("DBPORT","");
define("DBUSER", "docmgr");
define("DBPASSWORD", "");
define("DBNAME", "docmgr");
define("FILE_DIR", "%{_localstatedir}/lib/%{name}/files");
define("ADMIN_EMAIL", "root@localhost");
define("SITE_URL", "http://localhost/%{name}");
define("SITE_PATH", "%{webroot}");
define("IMPORT_DIR", FILE_DIR . "/import");
define("DB_CHARSET", "UTF-8");
define("VIEW_CHARSET", "UTF-8");
define("DEBUG", "5");
EOF

install -d %{buildroot}%{_sysconfdir}/sysconfig
tee %{buildroot}%{_sysconfdir}/sysconfig/%{name} << EOF
# OpenOffice.org
OOFFICE_HOST="localhost"
OOFFICE_PORT="8100"
# Any additional options to pass to ooffice can be set here
OOFFICE_OPTIONS="-norestore -nofirststartwizard -invisible -nodefault -nologo -nolockcheck"
EOF

find %{buildroot} -name \*~ |xargs rm -f

# ghost files
for conf in app-config.php config.php; do
	touch %{buildroot}%{webroot}/config/local/{,tmp/}$conf
done

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /sbin/nologin

%post
%_post_service %{name}

%postun
%_postun_userdel %{name}

%preun
%_preun_service %{name}

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
%config %{webroot}/config/vendor/config.php
%config(noreplace) %{webroot}/config/ldap-config.php
%config(noreplace, missingok) %ghost %{webroot}/config/local/app-config.php
%config(noreplace, missingok) %ghost %{webroot}/config/local/config.php
%attr(775, root, apache) %dir %{webroot}/config/local/tmp/
%ghost %{webroot}/config/local/tmp/app-config.php
%ghost %{webroot}/config/local/tmp/config.php
#%attr(600, root, root) %config(noreplace, missingok) %ghost %{webroot}/config/ldap-config.php
%{webroot}/config/forms
%{webroot}/config/db_version.php
%{webroot}/config/*.xml
%{webroot}/controls
%{webroot}/header
%{webroot}/install
%{webroot}/javascript
%{webroot}/jslib
%{webroot}/lib
%{webroot}/modules
%{webroot}/themes
%{webroot}/sabredav
%{webroot}/scripts
%{webroot}/api.php
%{webroot}/history.php
%{webroot}/index.php
%{webroot}/webdav.php
%attr(711,docmgr,docmgr) %dir %{_localstatedir}/lib/%{name}
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}/files


%define	prerel	RC10
%define	webroot	%{_var}/www/docmgr

Name:		docmgr
Version:	1.0
Release:	0.%{prerel}.3
License:	GPLv2
Group:		System/Servers
Summary:	Web based DMS - Document Management System
URL:		http://docmgr.org/

Source0:	%{name}-%{version}%{?prerel:-%{prerel}}.tar.gz
Source1:	docmgr-rsync.sh
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
Patch42:	docmgr-1.0-RC10-use-improved-external-documentconverter.patch

Requires:	clamav
Requires:	enscript
Requires:	file
Requires:	gocr
Requires:	imagemagick
Requires:	libtiff-progs
Requires:	ocrad
Requires:	poppler
Requires:	python-odconverter
Requires:	sendmail-command
Requires:	xpdf
Requires:	xpdf-tools
Requires:	wget
Requires:	zip

Requires:	apache-mod_ssl
Requires:	mod_php
Requires:	php-cli
Requires:	php-iconv
Requires:	php-imap
Requires:	php-fileinfo
Requires:	php-mbstring
Requires:	php-pgsql
Requires:	php-zip

Requires:	postgresql-server >= 8.4
Requires:	postgresql-contrib-virtual
Requires:	postgresql-plpgsql-virtual
Requires(post,preun):	rpm-helper

BuildArch:	noarch

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
#%%patch38 -p1 -b .local_installer~
%patch39 -p1 -b .protected~
#%%patch40 -p1 -b .db_setup~
%patch41 -p1 -b .setup~
%patch42 -p1 -b .pyodconv_new~

find -type f |xargs chmod 644

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_var}/{www,lib}/docmgr
cp -r */ *.php %{buildroot}%{webroot}
rm -rf %{buildroot}%{webroot}/{DOCS,sd}
mv %{buildroot}%{webroot}/files %{buildroot}%{_var}/lib/%{name}

install -d %{buildroot}%{webappconfdir}
tee %{buildroot}%{webappconfdir}/%{name}.conf << EOF
Alias /%{name} %{webroot}
<Directory "%{webroot}">
  Require all granted
</Directory>

<Directory "%{webroot}/bin">
  Require all denied
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

tee %{buildroot}%{webroot}/config/vendor/app-config.php << EOF
<?php
/********************************************
  DO NOT EDIT THE SETTINGS IN THIS FILE (config/vendor/app-config.php)!
  Add your own local settings to config/local/app-config.php in stead,
  otherwise you might loose your configuration when upgrading.
********************************************/

define('OPENOFFICE_PATH', '');
EOF

find %{buildroot} -name \*~ |xargs rm -f

# ghost files
for conf in app-config.php config.php; do
	touch %{buildroot}%{webroot}/config/local/{,tmp/}$conf
done

install -m755 %{SOURCE1} -D %{buildroot}%{webroot}/bin/docmgr-rsync.sh

install -d %{buildroot}%{_sysconfdir}/logrotate.d
tee %{buildroot}%{_sysconfdir}/logrotate.d/docmgr-rsync <<EOH
%{_var}/log/docmgr/rsync.log {
    notifempty
    missingok
    copytruncate
}
EOH

install -m700 -d %{buildroot}%{_var}/log/docmgr

%posttrans
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc DOCS/AUTHORS 
%config %{webappconfdir}/%{name}.conf
%dir %{webroot}
%{webroot}/apilib
%{webroot}/app
%{webroot}/auth
%dir %{webroot}/bin
%attr(755,,root,root) %{webroot}/bin/*
%{webroot}/ckeditor
%dir %{webroot}/config
%config %{webroot}/config/app-config.php
%config %{webroot}/config/config.php
%dir %{webroot}/config/vendor
%config %{webroot}/config/vendor/app-config.php
%config %{webroot}/config/vendor/config.php
%config(noreplace) %{webroot}/config/ldap-config.php
%dir %{webroot}/config/local
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
%attr(711,root,root) %dir %{_localstatedir}/lib/%{name}
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}/files
%config(noreplace) %{_sysconfdir}/logrotate.d/docmgr-rsync
%attr(700,apache,apache) %{_var}/log/docmgr


%changelog
* Wed Oct 06 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-0.RC10.2mdv2011.0
+ Revision: 583623
- add a rsync script with logging for use with crontabs..
- be sure to own 'config/vendor' & 'config/local'
- add default 'config/vendor/app-config.php' for proper OOo defaults
- add 'php-cli' to dependencies
- add webapp scriptlet and corresponding rpm-helper dependencies
- drop user creation, docmgr no longer requires it's own as the OOo daemon runs
  under another user from another package now..
- get rid of internal DocumentConverter.py completely
- fix a typo in file-convert.php
- split out OOo conversion service and into 'python-odconverter' package

* Tue Jun 08 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-0.RC10.1mdv2010.1
+ Revision: 547254
- strip path from binary for checking..
- fix lock & subsys files..
- use new, external pyodconverter
- * more enhancements for installer:
 o all errors now gets printed at right places
 o configuration will now be stored in session without reloading
 o improved formatting etcetc..
- override DBPASSWORD to be empty, so that we don't get a default password
- force https through rewrite in apache config
- fix database creation & permission checks
- default to 'GMT' timezone if none set
- fix ghost file creation of config files
- clean up and assemble all configuration related patches into one
- ditch utf-8 patch, it's now dealt with in database initialization functions
- "steal" mediawiki's functions for initializing and setting up database(P40)
- make "/Users" protected
- add back check-bitset-not-bitmask patch, evidently it wasn't fixed after all..
- make sure that OPENOFFICE object actaully uses the symlink created...
- make installer use separate local/vendor configuration layout
- package is now noarch again and OOo dependencies has been moved out
- enable local & vendor configuration again
- change behaviour to create a symlink with the corresponding suffix to properly detect format based on it as mime type isn't always available... :/
- replace python code within script with external
- be sure to quote variables that's customizable when checking them in initscript
- add php-mbstring to requires
- new release: 1.0RC10
- regenerate or drop relevant patches
- Use host & port specified in /etc/sysconfig/docmgr if available for doc conversion (P37)
- properly exit with (verbosive) error when unable to connect to running instance
- add -nolockcheck to ooffice options
- add '-invisible -nodefault -nologo' to ooffice's options
- connect to postgresql through unix sockets by default rather than tcp/ip
- make pg_connect accept empty variables for it to fall back to defaults (P36)
- give a more verbosive status message when unable to connect
- remove init option from usage help as the plans for it were abandoned
- make python script more robust
- add service scriptlets
- replace hacky shell function to check if soffice.bin is running with a more pyuno based script
- start soffice.bin with '-norestore -nofirststartwizard'
- don't prefix pid file with docmgr- anymore as it's in it's own docmgr directory
- fix so that we get the right date printed for date due of tasks
- display recipient notes for workflow tasks
- set comment for workflow route properly
- add missing objectId to edittask query
- fix so that account gets updated when selecting it from drop down under "Reset
  Password" as well
- Split date and time in php for workflow to get it localized format correct (P0)
- redo user list patch to be in javascript so it'll be updated on the fly
- set default permissions to INSERT_OBJECTS for new users (P31)
- fix accidentally commited part of patch
- we really need postgresql 8.4 as prefix searching with tsearch2 and also
  plpgsql functions requires it
- new release: 1.0RC9
- fix init script to properly check status
- fix finfo() backwards compatibility with php < 5.3.0
- install all scripts
- add a couple of more dependencies on OOo to support more formats
- fix relative path for some backgrounds in css files..
- update restricted patch to work with RC8
- check that bitset (which actually exists in the table) and not bitmask is null
- fix setting of bitmask (P28)
- add a user list to the account manager (P27)
- update to ckeditor 3.2 (P26)
- add support for prefix search with tsearch2 (P25)
- remove part of patch that originates from other patch applied later
- update no_temp patch to check file types based on mime type rather than file extension
- Print out the actual error message during first login (P24)
- set baseUri for webdav to work without a "reserved domain" by default
- run indexer as admin (P22)
- use utf-8 for client_encoding (P21)
- update to 1.0RC8
- regenerate patches needed and drop those we no longer need
- check exit status of OOo converter (P20)
- update more mimetypes...
- reenable P8
- make sure that we're looking for our config files in the right directories...
- Add absolute path to include_path (P19)
- fix incorrect mime_type used for .docx documents
- disable P8 for now...
- * process correct document file from the correct location (updates P8)
  * don't use temp ("worker") file for for thumbnails either (updates P8)
- fix a typo (P17)
- fix path used used in process.php (P16)
- fix setting of include_path (updates P0)
- implement missing RESTRICTED_DELETE functionality
- Check that user actually exists before trying to update failed_logins for it (P14)
- set default timezone if defined (P13)
- adjust dependencies
- add dependency on openoffice.org-writer for doc conversion
- fix path to IMPORT_DIR
- change attributes for local configuration directory to be more restrictive
- fix OOo dependency for 2009.0/MES5 backport...
- docmgr needs a writable home directory
- pass home dir & shell to %%_pre_useradd
- if no config found, add a link or instructions on front page
- die if unable to connect to postgresql (P12)
- add php header to vendor configuration
- add a conditionalInclude() function to avoid dependencies getting added (P11)
- ditch unused functions for mediawiki derived installer
- %{webroot}/config/vendor/config.php should of course not be a ghost file
- improve work on tracing the process started and whether it's succesful or not
  (WIP)
- don't exit init script if sysconfig file is missing, default variables are
  carried in init script anyways now
- give init script a bit more descriptive name to use when printing messages
- add initial progress with a web ui based installer based on mediawiki's
- remove any attempts on doing initialization & configuration from init script
- * define TMP_DIR only once in config/config.php
  * use require_once() rather than include() to avoid conflicts
- * add support for a vendor provided configuration
  * use require_once() rather than include() to avoid config file conflicts
- Use LC_TIME for date & time format if LOCALE is set (P9)
- start on setup script
- fix %%config in %%files
- cosmetics
- make it possible to override all configuration files with a local version (P0)
- in stead of editing config file with our own settings, load them from an
  optional config/localconfig.php file in stead (replaces P0)
- try look for OOo python module directory in OPENOFFICE_PATH (updates P6)
- don't use a temporary copy of input document for conversion (P8)
- fix so that relative site_url is used for closeKeepAlive() (P7)
- import docmgr


* Mon Feb 22 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-0.RC6.1
- initial release (work in progress...)

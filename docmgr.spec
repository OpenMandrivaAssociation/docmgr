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
Source7:	docmgr.init
Source8:	docmgr.sysconfig
Patch0:		docmgr-1.0-RC6-config-mdkconf.patch
Patch1:		docmgr-1.0-RC6-unified-tmpdir.patch
Patch2:		docmgr-1.0-RC6-quiet-rm.patch
Patch3:		docmgr-1.0-RC6-no-dos-eol.patch
Patch4:		docmgr-1.0-RC6-PyODConverter-1.1.patch
Patch5:		docmgr-1.0-RC6-PyODConvert-stream.patch
Patch6:		docmgr-1.0-RC6-fileconvert-ooo-profile.d.patch

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
%patch0 -p1 -b .mdkconf~
%patch1 -p1 -b .tmpdir~
%patch2 -p1 -b .quiet~
%patch3 -p1 -b .dos_eol~
%patch4 -p1 -b .doc_conv1.1~
%patch5 -p1 -b .stream~
%patch6 -p1 -b .ooo~
sed -e 's#postgres#docmgr#g' -i scripts/docmgr.pgsql

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_var}/{www,lib}/docmgr
cp -r */ *.php %{buildroot}%{webroot}
rm -rf %{buildroot}%{webroot}/{DOCS,scripts}
mv %{buildroot}%{webroot}/files %{buildroot}%{_var}/lib/docmgr

install -m755 %{SOURCE7} -D %{buildroot}%{_initrddir}/docmgr
install -m644 %{SOURCE8} -D %{buildroot}%{_sysconfdir}/sysconfig/docmgr
install -m644 scripts/docmgr.pgsql -D %{buildroot}%{_datadir}/docmgr/docmgr.pgsql

install -d %{buildroot}%{webappconfdir}
tee %{buildroot}%{webappconfdir}/docmgr.conf << EOF
Alias /docmgr %{webroot}
<Directory "%{webroot}">
  Order allow,deny
  Allow from All
</Directory>

<Directory "%{webroot}/bin">
  Order allow,deny
  Deny from All
</Directory>
EOF

find %{buildroot} -name \*~ |xargs rm -f

%pre
%_pre_useradd %{name}

%postun
%_postun_userdel %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc DOCS/AUTHORS 
%{_initrddir}/docmgr
%dir %{_datadir}/docmgr
%{_datadir}/docmgr/docmgr.pgsql
%config(noreplace) %{_sysconfdir}/sysconfig/docmgr
%config(noreplace) %{webappconfdir}/docmgr.conf
%dir %{webroot}
%{webroot}/*
%attr(-,apache,apache) %{_localstatedir}/lib/docmgr/files 


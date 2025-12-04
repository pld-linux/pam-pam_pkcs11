#
# Conditional build:
%bcond_without	curl	# cURL support
%bcond_without	ldap	# LDAP support (via OpenLDAP)
%bcond_with	nss	# NSS instead of OpenSSL
%bcond_without	pcsc	# PC/SC Lite support

Summary:	PAM login module that allows a X.509 certificate based user login
Summary(pl.UTF-8):	Moduł PAM umożliwiający logowanie się w oparciu o certyfikat X.509
Name:		pam-pam_pkcs11
Version:	0.6.13
Release:	3
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/OpenSC/pam_pkcs11/releases
Source0:	https://github.com/OpenSC/pam_pkcs11/archive/pam_pkcs11-%{version}.tar.gz
# Source0-md5:	329426f89f13a5374828c35199c54d73
Patch0:		systemdunitdir.patch
URL:		https://github.com/OpenSC/pam_pkcs11
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
%{?with_curl:BuildRequires:	curl-devel}
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	libxslt-progs
BuildRequires:	libtool >= 2:2
%{?with_nss:BuildRequires:	nss-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.4.6}
%{!?with_nss:BuildRequires:	openssl-devel}
BuildRequires:	pam-devel
%{?with_pcsc:BuildRequires:	pcsc-lite-devel >= 1.6.0}
BuildRequires:	pkgconfig
%{?with_pcsc:Requires:	pcsc-lite-libs >= 1.6.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}

%description
This PAM login module allows a X.509 certificate based user login. The
certificate and its dedicated private key are thereby accessed by
means of an appropriate PKCS#11 module. For the verification of the
users' certificates, locally stored CA certificates as well as either
online or locally accessible CRLs are used.

%description -l pl.UTF-8
Ten moduł PAM umożliwia logowanie się w oparciu o certyfikaty X.509.
Certyfikat i jego klucz prywatny są odczytywane poprzez odpowiedni
moduł PKCS#11. Do weryfikacji certyfikatów użytkowników używane są
lokalnie przechowywane certyfikaty CA albo dostępne lokalnie lub
zdalnie CRL.

%prep
%setup -q -n pam_pkcs11-pam_pkcs11-%{version}
%patch -P0 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I aclocal
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_curl:--with-curl} \
	%{!?with_ldap:--without-ldap} \
	%{?with_nss:--with-nss} \
	%{!?with_pcsc:--without-pcsclite}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_pkcs11.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pam_pkcs11/*.la
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/pam_pkcs11/*.example

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{README.*,*.html,*.css} etc/*.example
%attr(755,root,root) %{_bindir}/card_eventmgr
%attr(755,root,root) %{_bindir}/pkcs11_eventmgr
%attr(755,root,root) %{_bindir}/pkcs11_inspect
%attr(755,root,root) %{_bindir}/pkcs11_listcerts
%attr(755,root,root) %{_bindir}/pkcs11_make_hash_link
%attr(755,root,root) %{_bindir}/pkcs11_setup
%attr(755,root,root) %{_bindir}/pklogin_finder
%{_libdir}/security/pam_pkcs11.so
%dir %{_libdir}/pam_pkcs11
%{_libdir}/pam_pkcs11/*.so
%{systemdunitdir}/pkcs11-eventmgr.service
%{_mandir}/man1/card_eventmgr.1*
%{_mandir}/man1/pkcs11_*.1*
%{_mandir}/man1/pklogin_finder.1*
%{_mandir}/man8/pam_pkcs11.8*

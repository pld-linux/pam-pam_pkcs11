Summary:	PAM login module that allows a X.509 certificate based user login
Summary(pl.UTF-8):	Moduł PAM umożliwiający logowanie się w oparciu o certyfikat X.509
Name:		pam-pam_pkcs11
Version:	0.6.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opensc-project.org/files/pam_pkcs11/pam_pkcs11-%{version}.tar.gz
# Source0-md5:	5f3be860fa5b630cbce113e4a9bc6996
Source1:	pam_pkcs11.pl.po
URL:		http://www.opensc-project.org/pam_pkcs11/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	gettext-devel >= 0.16.1
BuildRequires:	libxslt-progs
BuildRequires:	libtool
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
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
%setup -q -n pam_pkcs11-%{version}

cp -f %{SOURCE1} po/pl.po
sed -i -e 's/"fr"/"fr pl"/' configure.in
rm -f po/stamp-po

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I aclocal
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-curl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/pam_pkcs11/*.{la,a}

%find_lang pam_pkcs11

%clean
rm -rf $RPM_BUILD_ROOT

%files -f pam_pkcs11.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{README.*,*.html,*.css} etc/*.example
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /%{_lib}/security/pam_pkcs11.so
%dir %{_libdir}/pam_pkcs11
%attr(755,root,root) %{_libdir}/pam_pkcs11/*.so
%{_mandir}/man[18]/*

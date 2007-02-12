Summary:	PAM login module that allows a X.509 certificate based user login
Summary(pl.UTF-8):   Moduł PAM umożliwiający logowanie się w oparciu o certyfikat X.509
Name:		pam-pam_pkcs11
Version:	0.5.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opensc-project.org/files/pam_pkcs11/pam_pkcs11-%{version}.tar.gz
# Source0-md5:	607e3ba84b8938eff20c51c597e522c0
URL:		http://www.opensc-project.org/pam_pkcs11/
BuildRequires:	curl-devel
BuildRequires:	libxslt-progs
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
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

%build
%configure \
	--with-curl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/pam_pkcs11/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{README.*,*.html,*.css} etc/*.example
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /%{_lib}/security/pam_pkcs11.so
%dir %{_libdir}/pam_pkcs11
%attr(755,root,root) %{_libdir}/pam_pkcs11/*.so
%{_mandir}/man[18]/*

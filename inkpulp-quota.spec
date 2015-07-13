Name:		inkpulp-quota
Version:	1.0.2
Release:	1%{?dist}
Summary:	A quota checking tool for PaperCut servers.

Group:		Applications/System
License:	GPL
URL:		UNKNOWN
Source0:	inkpulp-quota-1.0.2.tar.gz

#BuildRequires:	
#Requires:	

%description
InkPulp-Quota (ipq) is a very simple tool that 
allows Linux users to query their remaining 
quota on PaperCut servers from the command line.

%prep
%setup -q

%build

%install
mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/usr/share/inkpulp-quota
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
cp inkpulp-quota.yml ${RPM_BUILD_ROOT}/etc/
cp inkpulp-quota.pyo ${RPM_BUILD_ROOT}/usr/share/inkpulp-quota/
cp inkpulp-quota.sh ${RPM_BUILD_ROOT}/usr/share/inkpulp-quota/
ln -s /usr/share/inkpulp-quota/inkpulp-quota.sh ${RPM_BUILD_ROOT}/usr/bin/ipq

%files
%config /etc/inkpulp-quota.yml
/usr/share/inkpulp-quota/inkpulp-quota.pyo
/usr/share/inkpulp-quota/inkpulp-quota.sh
/usr/bin/ipq

%changelog


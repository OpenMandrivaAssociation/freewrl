In order for the java classes to do anything, they need to be able to talk to the freewrl binary via a tcp port; which requires a java policy modification.
A policy file (java.policy) is included in /usr/share/freewrl/. To use it, either use policytool from the Java JRE or copy it to ~/java.policy

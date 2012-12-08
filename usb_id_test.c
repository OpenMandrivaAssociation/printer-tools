/* Test program to try to query device id from printer. */

#include <stdio.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>

#define IOCNR_GET_DEVICE_ID	1
#define LPIOC_GET_DEVICE_ID(len) _IOC(_IOC_READ, 'P', IOCNR_GET_DEVICE_ID, len)	/* get device_id string */
#define LPGETSTATUS		0x060b		/* same as in drivers/char/lp.c
 */

int
main (int argc, char **argv)
{
  const char *fn;
  int fd;
  unsigned char argp[1024];
  int length;
  unsigned char status;

  if (argc != 2)
    {
      fprintf (stderr, "usage: usb_id_test /dev/usb/lp0\n");
      return 1;
    }
  fn = argv[1];
  fd = open (fn, O_RDWR);
  if (fd < 0)
    {
      fprintf (stderr, "Error opening %s: %s\n",
	       fn, strerror (errno));
      return 1;
    }
  if (ioctl (fd, LPIOC_GET_DEVICE_ID(sizeof(argp)), argp) < 0)
    {
      fprintf (stderr, "Error doing ioctl: %s\n",
	       strerror (errno));
      return 1;
    }
  length = (argp[0] << 8) + argp[1] - 2;
  printf ("GET_DEVICE_ID string:\n");
  fwrite (argp + 2, 1, length, stdout);
  printf ("\n");
  if (ioctl (fd, LPGETSTATUS, &status) < 0)
    {
      fprintf (stderr, "Error doing ioctl: %s\n",
	       strerror (errno));
      return 1;
    }
  printf ("Status: 0x%02x\n", status);
  close (fd);
  return 0;
}

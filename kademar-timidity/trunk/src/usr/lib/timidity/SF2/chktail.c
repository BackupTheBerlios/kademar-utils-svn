#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>

#define TAIL 56

void main(int argc, char** argv)
{
    int i, j;
    signed char buff[TAIL];

    for(i = 1; i < argc; i++)
    {
	char* f;
	int fd;

	f = argv[i];
	if((fd = open(f, O_RDWR)) < 0)
	{
	    perror(f);
	    continue;
	}

	lseek(fd, -TAIL, SEEK_END);
	read(fd, buff, TAIL);
	printf("%s: ", f);
	for(j = 0; j < TAIL; j++)
	    if(buff[j] < ' ')
		putchar('.');
	    else
		putchar(buff[j]);
	putchar('\n');
	close(fd);
    }
}



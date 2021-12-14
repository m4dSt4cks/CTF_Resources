#include <stdio.h>
#include <stdlib.h>

#define NUM_POINTERS 64


void main() {
	// Disable buffering of I/O so that doesn't mess with heap
	setbuf(stdout, NULL);
	setbuf(stdin, NULL);
	
	char *pointers[NUM_POINTERS];
	int option = 0;
	int size = 0;
	
	int i = 0;
	for (i = 0; i < NUM_POINTERS; i++) {
		pointers[i] = NULL;
	}
	
	while (1) {
		printf("1) malloc\n2) free\n3) show\n4) exit\n> ");
		scanf("%zu", &option);
		switch (option) {
			case 1:								
				printf("Index? ");
				scanf("%zu", &option);
				if (option < NUM_POINTERS && pointers[option] == NULL) {
					printf("Bytes? ");
					scanf("%zu", &size);
					pointers[option] = malloc(size);
					if (pointers[option]) {
						printf("Mallocing %p\n", pointers[option]);
						for (i = 0; i < size; i++) {
							pointers[option][i] = "A";
						}
					} else {
						printf("Malloc error!\n");
					}
				} else {
					printf("Invalid index\n");
				}
				break;
			case 2:
				printf("Index? ");
				scanf("%zu", &option);
				if (option < NUM_POINTERS) {
					printf("Freeing %p\n", pointers[option]);
					free(pointers[option]);
					pointers[option] = NULL;
				} else {
					printf("Invalid index\n");
				}
				break;
			case 3:
				printf("-----Pointers-----\n");
				for (i = 0; i < NUM_POINTERS; i++) {
					printf("%zu: %p\n", i, pointers[i]);
				}
				break;
			case 4:
				return;
			default:
				printf("Invalid option\n");
		}
		printf("\n\n");
	}
}

// gcc practice.c -o practice -no-pie -m64

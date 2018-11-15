#include "trace.h"
//#include "pybthread.h"

#define MICROPY_PY_DEBUG

extern fs_user_mount_t *fs_user_mount_flash; 
FIL trace_log_fp;

#if 0 // mark useless trace log func

#include "trace.h"
#include <stdint.h>
#include STM32_HAL_H

#define TRACEBUF_SIZE   (256)
typedef struct _tracebuf_t {
    uint8_t idx;
    uint8_t buf[TRACEBUF_SIZE];
} tracebuf_t;

static tracebuf_t tracebuf;

void trace_init()
{
    tracebuf.idx = 0;
    for (int i=0; i<TRACEBUF_SIZE; i++) {
        tracebuf.buf[i] = 0;
    }
}

void trace_insert(uint32_t x)
{
    __disable_irq();
    if (tracebuf.idx < TRACEBUF_SIZE) {
        tracebuf.buf[tracebuf.idx++] = x;
    }
    __enable_irq();
}
#endif 


#ifdef MICROPY_PY_DEBUG
int trace_init() {
	FRESULT ret;

	ret = f_open(&fs_user_mount_flash->fatfs, &trace_log_fp, "/trace.log", FA_WRITE | FA_OPEN_APPEND);
	if(ret == FR_OK)
		return 0;
	else if(ret == FR_NO_FILE){
		ret = f_open(&fs_user_mount_flash->fatfs, &trace_log_fp, "/trace.log", FA_WRITE | FA_CREATE_NEW);
		if(ret == FR_OK)
			return 0;
		else 
			return 1;
	}
	else 
		return 1;

//	pyb_mutex_init(&thread_mutex);
}

int trace_write(char* fmt, ...){

	if(fmt == NULL)
		return 1;

	va_list arg_ptr;
	char buf[TRACE_BUFFER_SIZE_C];
	
//    pyb_mutex_lock(&thread_mutex, 1);

	memset(buf, 0, sizeof(buf));

	va_start(arg_ptr, fmt);
	vsnprintf(&buf[strlen(buf)], sizeof(buf) - strlen(buf), fmt, arg_ptr);
	va_end(arg_ptr);

	UINT n;
	f_write(&trace_log_fp, buf, strlen(buf), &n);
	if(n != strlen(buf))
		return 1;
	f_sync(&trace_log_fp);

//    pyb_mutex_unlock(&thread_mutex);

	return 0;
}

int trace_deinit() {
	f_close(&trace_log_fp);

	return 0;
}
#else
int trace_init() {
	return 0;
}

int trace_write(char* fmt, ...) {
	return 0;
}
int trace_deinit() {
	return 0;
}
#endif

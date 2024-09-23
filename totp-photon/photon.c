#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "photon.h"

#if defined(_PHOTON160_)
#define D 7
#define S 4
#define N 40 // 160/S
#define R 9  // 36/S
const int IC[] = {0, 1, 2, 5, 3, 6, 4};
const int M[D][D] = {
    {1, 4, 6, 1, 1, 6, 4},
    {4, 2, 15, 2, 5, 10, 5},
    {5, 3, 15, 10, 7, 8, 13},
    {13, 4, 11, 2, 7, 15, 9},
    {9, 15, 7, 2, 11, 4, 13},
    {13, 8, 7, 10, 15, 3, 5},
    {5, 10, 5, 2, 15, 2, 4}};

#elif defined(_PHOTON224_)
#define D 8
#define S 4
#define N 56 // 224/S
#define R 8  // 32/S
const int IC[] = {0, 1, 3, 7, 15, 14, 12, 8};
const int M[D][D] = {
    {2, 4, 2, 11, 2, 8, 5, 6},
    {12, 9, 8, 13, 7, 7, 5, 2},
    {4, 4, 13, 13, 9, 4, 13, 9},
    {1, 6, 5, 1, 12, 13, 15, 14},
    {15, 12, 9, 13, 14, 5, 14, 13},
    {9, 14, 5, 15, 4, 12, 9, 6},
    {12, 2, 2, 10, 3, 1, 1, 14},
    {15, 1, 13, 10, 5, 10, 2, 3}};

#elif defined(_PHOTON256_)
#define D 6
#define S 8
#define N 32 // 256/S
#define R 4  // 32/S
const int IC[] = {0, 1, 3, 7, 6, 4};
const int M[D][D] = {
    {2, 3, 1, 2, 1, 4},
    {8, 14, 7, 9, 6, 17},
    {34, 59, 31, 37, 24, 66},
    {132, 228, 121, 155, 103, 11},
    {22, 153, 239, 111, 144, 75},
    {150, 203, 210, 121, 36, 167}};

#endif

#if defined(_PHOTON160_) || defined(_PHOTON224_)
#define ReductionPoly 0x3;
#define padVal 0x8
int sbox[] = {12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2};

#elif defined(_PHOTON256_)
#define ReductionPoly 0x1b;
#define padVal 0x80
int sbox[] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16};
#endif

int RC[] = {1, 3, 7, 14, 13, 11, 6, 12, 9, 2, 5, 10};

int fieldMult(int a, int b)
{
    int x = a, ret = 0;
    int i;
    for (i = 0; i < S; i++)
    {
        if ((b >> i) & 1)
        {
            ret ^= x;
        }
        if ((x >> (S - 1)) & 1)
        {
            x <<= 1;
            x ^= ReductionPoly;
        }
        else
        {
            x <<= 1;
        }
    }
    return ret & (1 << S) - 1;
}

void addConstant(int State[D][D], int k)
{
    for (int i = 0; i < D; i++)
    {
        State[i][0] = State[i][0] ^ RC[k] ^ IC[i];
    }
}

void subCells(int State[D][D])
{
    for (int i = 0; i < D; i++)
        for (int j = 0; j < D; j++)
            State[i][j] = sbox[State[i][j]];
}

void shiftRows(int State[D][D])
{
    int i, j;
    int tmp[D];
    for (i = 1; i < D; i++)
    {
        for (j = 0; j < D; j++)
            tmp[j] = State[i][j];
        for (j = 0; j < D; j++)
            State[i][j] = tmp[(j + i) % D];
    }
}

void mixColumnsSerial(int State[D][D])
{
    int tmp[D];
    for (int j = 0; j < D; j++)
    {
        for (int i = 0; i < D; i++)
        {
            int sum = 0;
            for (int k = 0; k < D; k++)
            {
                sum ^= fieldMult(M[i][k], State[k][j]);
            }
            tmp[i] = sum;
        }
        for (int i = 0; i < D; i++)
        {
            State[i][j] = tmp[i];
        }
    }
}

void permutation(int State[D][D])
{
    for (int i = 0; i < 12; i++)
    {
        addConstant(State, i);
        subCells(State);
        shiftRows(State);
        mixColumnsSerial(State);
    }
}

int photon(int *msg, int msgLength, int *digest)
{
    #if defined(_PHOTON160_)
int State[D][D] = {
    {0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0},
    {0, 2, 8, 2, 4, 2, 4},
};

#elif defined(_PHOTON224_)
int State[D][D] = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 3, 8, 2, 0, 2, 0},

};
#elif defined(_PHOTON256_)

int State[D][D] = {
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0x40, 0x20, 0x20}

};
#endif
    int remains = R - (msgLength % R);
    int paddedLength = msgLength + remains;
    int paddedMsg[paddedLength];
    memset(paddedMsg, 0x00, paddedLength * sizeof(int));
    memcpy(paddedMsg, msg, msgLength * sizeof(int));
    paddedMsg[msgLength] = padVal;
    int i = 0;
    while (i < paddedLength)
    {
        for (int j = 0; j < R; j++)
        {
            State[0][j] ^= paddedMsg[i++];
        }

        if (i % R != 0)
        { // PHOTON160
            State[1][0] ^= paddedMsg[i++];
            State[1][1] ^= paddedMsg[i++];
        }
        for (int j = 0; j < D; j++)
        {
        }

        permutation(State);
    }
    i = 0;
    int digestLength = 0;
    while (digestLength < N)
    {
        for (int j = 0; j < R; j++)
        {
            digest[i++] = State[0][j];
        }

        if (i % R != 0)
        { // PHOTON160
            digest[i++] = State[1][0];
            digest[i++] = State[1][1];
        }
        permutation(State);
        digestLength += R;
    }
}

int hash(int *msgBytes, int msgBytesLength, int *digestByte, int byteSize)
{
    int digest[N];

#if defined(_PHOTON160_) || defined(_PHOTON224_)
    int msgLength = msgBytesLength * 2;
    int msg[msgLength];
    int j = 0;
    for (int i = 0; i < msgBytesLength; i++)
    {
        msg[j++] = msgBytes[i] / 16;
        msg[j++] = msgBytes[i] % 16;
    }
    photon(msg, msgLength, digest);
    j = 0;
    for (int i = 0; i < byteSize; i++)
    {
        digestByte[i] = digest[j++] * 0x10 + digest[j++];
    }
#elif defined(_PHOTON256_)
    photon(msgBytes, msgBytesLength, digestByte);
#endif

    return 0;
}
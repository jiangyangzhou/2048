#include "curand_kernel.h" 
#include <iostream>
#include "gputimer.h"
#include <stdio.h>

//#include <time>

using namespace std;
__device__ int combine(int * l_state, int turn){
    int score=0;
    bool if_move=false; 

    if (turn==0){ //left
        for(int i=0;i<4;i++){
            for(int t=0;t<3;t++){
                int j =0, k=0;
                if(t!=1){
                    for(j=0;j<4;j++){
                        if(l_state[4*i+j]!=0){
                            l_state[4*i+k]=l_state[4*i+j];
                            k++;
                        }
                    }
                    while(k<4){l_state[4*i+k]=0; k++; if_move = true;}
                }
                else
                    for(j=0;j<3;j++){
                        if(l_state[4*i+j] && l_state[4*i+j]==l_state[4*i+j+1]){
                            l_state[4*i+j]+=1;
                            score+=1;
                            l_state[4*i+j+1]=0;
                            j++;
                        }
                    }
            }
        }
    }
    if (turn==1){  //down
        for(int j=0;j<4;j++){
            for(int t=0;t<3;t++){
                int i =3, k=3;
                if(t!=1){
                    for(i=3;i>=0;i--){
                        if(l_state[4*i+j]!=0){
                            l_state[4*k+j]=l_state[4*i+j];
                            k--;

                        }
                    }
                    while(k>=0){l_state[4*k+j]=0; k--; if_move = true;}
                }
                else
                    for(i=3;i>=0;i--){
                        if(l_state[4*i+j] && l_state[4*i+j]==l_state[4*(i-1)+j]){
                            l_state[4*i+j]+=1;
                            score+=1;
                            l_state[4*(i-1)+j]=0;
                            i--;
                        }
                    }
            }
        }
    }
    if (turn==2){   //right
        for(int i=0;i<4;i++){
            for(int t=0;t<3;t++){
                int j =3, k=3;
                if(t!=1){
                    for(j=3;j>=0;j--){
                        if(l_state[4*i+j]!=0){
                            l_state[4*i+k]=l_state[4*i+j];
                            k--;
                        }
                    }
                    while(k>=0){l_state[4*i+k]=0; k--; if_move = true;}
                }
                else
                    for(j=3;j>0;j--)
                        if(l_state[4*i+j] && l_state[4*i+j]==l_state[4*i+j-1]){
                            l_state[4*i+j]+=1;
                            score+=1;
                            l_state[4*i+j-1]=0;
                            j--;
                        }
            }
        }
    }
    if (turn==3){//up
        for(int j=0;j<4;j++){
            for(int t=0;t<3;t++){
                int i =0, k=0;
                if(t!=1){
                    for(i=0;i<4;i++){
                        if(l_state[4*i+j]!=0){
                            l_state[4*k+j]=l_state[4*i+j];
                            k++;
                        }
                    }
                    while(k<4){l_state[4*k+j]=0; k++; if_move = true;}
                }
                else
                    for(i=0;i<3;i++){
                        if(l_state[4*i+j] && l_state[4*i+j]==l_state[4*(i+1)+j]){
                            l_state[4*i+j]+=1;
                            score+=1;
                            l_state[4*(i+1)+j]=0;
                            i++;
                        }
                    }
            }
        }
    }
    return score;
}


// over:0
__device__ int judge_over(const int *state)
{
    //bool alive=false;
    int zero_num=0;
    bool can_combine = false;
    for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
            if(state[4*i+j]==0) zero_num+=1;
            if(i<3 && j<3 && (state[4*i+j]==state[4*i+j+1] || state[4*i+j]==state[4*(i+1)+j]))
                can_combine=true;
        }
    }
    if(zero_num==0){
        if(!can_combine) return -1;
        else return zero_num;
    }            
    return true;
}

__device__ curandState newBlock(int * state, curandState curand_state, int No)
{

    int new_num=1;
    int r_num = curand(&curand_state)%10;
    if(r_num>8) new_num=2;
    bool ok=false;
    while(!ok){
        int r_place = curand(&curand_state)%16;
        //printf("No is %d, r_num is %d, r_place is %d \n", No, r_num, r_place);
        if(state[r_place]==0){
            state[r_place]=new_num;
            ok=true;
        }
    } 
    return curand_state;
}

__device__ void print_array(int *array, int size){
    for(int i=0; i<size; i++)
        printf("%d, ",array[i]);
    printf("\n");
}

__global__ void run_2048(const int * d_state, int *d_result, int search_depth, long seed ){
    int No = blockIdx.x * blockDim.x + threadIdx.x; 

    curandState curand_state;
    curand_init(seed-No, 0 ,0, &curand_state);

    int tid  = threadIdx.x;

    int init_state = threadIdx.x;
    int depth = search_depth;

    int  l_state[16];
    for(int i=0;i<16;i++)
        l_state[i] = d_state[i];
    int result=1;
    int score=0;
    int turn =0;
    int zero_num=16;

    while(depth && zero_num!=-1)
    {           
        zero_num = judge_over(l_state);
        if(zero_num>0)
            curand_state=newBlock(l_state, curand_state,No);
        turn = init_state%4;
        init_state/=4;
        depth-=1;
        result=combine(l_state, turn);
        score+=result;
    }

    int count=0;
    while(zero_num!=-1){
        count+=1;
        zero_num= judge_over(l_state);
        if(zero_num>0)
            curand_state=newBlock(l_state, curand_state,No);
        turn = curand(&curand_state)%4;
        result=combine(l_state, turn);
        score+=result;
    }
    atomicAdd(&(d_result[tid]),score);
    
 /*   printf("score3 is %d \n",score);
    printf("zero_num : %d \n",zero_num);
    printf("Block_id:%d, threadIdx.x: %d, atomicAdd:%d \n", 
                blockIdx.x, threadIdx.x, d_result[threadIdx.x]);
    print_array(l_state,16);*/
    
}

__global__ void setup_kernel ( curandState * state, unsigned long seed )
{
    int id = threadIdx.x  + blockIdx.x * blockDim.x;
    curand_init ( seed, id , 0, &state[id] );
}


void print_array2(int *array, int size){
    for(int i=0; i<size; i++)
        printf("%d, ",array[i]);
    printf("\n");
}

int get_best_turn(int *h_state, int exp_num=1000, int search_depth=2){
    int *d_state;
    //int h_state[16]={0};

    const int ARRAY_BYTES = 16*sizeof(int);
    cudaMalloc((void **) &d_state, ARRAY_BYTES);
    cudaMemset((void **) d_state, 0, ARRAY_BYTES);
    cudaMemcpy(d_state, h_state, ARRAY_BYTES, cudaMemcpyHostToDevice);

    long clock_for_rand = clock();

    const int search_kinds = (1<<(search_depth*2));

    int *d_result;
    int *h_result=new int[search_kinds];
    const int RESULT_BYTES = search_kinds*sizeof(int);
    for(int i=0; i<search_kinds; i++) h_result[i]=0;

    cudaMalloc((void **) &d_result, RESULT_BYTES); 
    cudaMemset((void **) d_result, 0, RESULT_BYTES);
    cudaMemcpy(d_result, h_result, RESULT_BYTES , cudaMemcpyHostToDevice);

    //timer.Start();
    run_2048<<<exp_num, search_kinds >>>(d_state, d_result, search_depth, clock_for_rand);
    //timer.Stop();

    cudaMemcpy(h_result, d_result, RESULT_BYTES, cudaMemcpyDeviceToHost);

    int max=0;
    int best_way=0;
    for(int i=0;i<search_kinds;i++){
        if(h_result[i]>max){
            max = h_result[i];
            best_way = i;
        }
    }

    int best_turn = best_way%4;

    print_array2(h_result, search_kinds);

    printf("Best way is %d , Best score = %d , Best turn is %d \n", 
                best_way, h_result[best_way], best_turn);

    cudaFree(d_state);
    cudaFree(d_result);
    return best_turn;
}


int main(int argc,char *argv[]){
 //   printf("Total amount of global memory: %d bytes",deviceProp.total)


    GpuTimer timer;

    int *d_state;
    int h_state[16]={0};

    const int ARRAY_BYTES = 16*sizeof(int);
    cudaMalloc((void **) &d_state, ARRAY_BYTES);
    cudaMemset((void **) d_state, 0, ARRAY_BYTES);

    long clock_for_rand = clock();
    cout<<"get arg num is "<<argc<<endl;

    int i=0, k=0;
    while(argc>1 && argv[1][i]!='\0')
    {
        if(argv[1][i]!=',')
            h_state[k]=h_state[k]*10+argv[1][i]-'0';
        else{
            k+=1;
            if(k>=16)
                cout<<"num of number exceed 16!"<<endl;
        }
        i=i+1;
    }
    cout<<"input h_state is:";
    print_array2(h_state,16);


    timer.Start();
    get_best_turn(h_state,10000,2);
    timer.Stop();

    //cudaMemcpy(h_state, d_state, ARRAY_BYTES, cudaMemcpyDeviceToHost);

    printf("Time elapsed = %g ms\n", timer.Elapsed());
    return 0;
}
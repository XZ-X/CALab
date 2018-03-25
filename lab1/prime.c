#include<stdio.h>

int isPrime(int x){
	if(x==2){
		return 1;
	}
	for(int i=3;i<x;i++){
		if(x%i==0)
				return 0;
	}
	return 1;
}


int prime(){
	char nums[1000000]={1};
	int cnt=0;
	for(int i=2;i<1000000;i++){
		if((nums[i]==0) && isPrime(i) ){
				cnt++;
				for(int j=i;j<1000000;j+=i){
						nums[j]=1;
				}
		}
	}
	return cnt;
}



int main(){
	printf("%d",prime());
	return 0;
}



#include <cmath>
#include <ctgmath>
#include <algorithm>
#include <utility>
#include <map>

#define _EVALUATE_

using namespace std;

typedef vector<int> UserRank; //lista de book ids, já ordenada
typedef map<int, UserRank> Ranks; //<id do usuario, UserRank>
typedef map<int, UserRank>::iterator RanksIt;

double NDCG(Ranks predictions, Ranks answers, Graph &G2);

void evaluate(Ranks R, Graph &G2);

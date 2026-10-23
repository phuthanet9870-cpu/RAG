function bfsPath(sx,sy,gx,gy){
 const C=W.cols,R=W.rows,S=W.solid;if(!S||sx<0||sy<0||gx<0||gy<0||sx>=C||gx>=C||sy>=R||gy>=R)return null;
 const prev=new Int32Array(C*R).fill(-2),queue=new Int32Array(C*R),start=sy*C+sx,goal=gy*C+gx;let head=0,tail=1,found=false;queue[0]=start;prev[start]=-1;
 const dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]];
 while(head<tail){const cur=queue[head++];if(cur===goal){found=true;break}const cx=cur%C,cy=Math.floor(cur/C);
  for(const[dx,dy]of dirs){const x=cx+dx,y=cy+dy;if(x<0||y<0||x>=C||y>=R)continue;const k=y*C+x;if(prev[k]!==-2||S[k])continue;if(dx&&dy&&(S[cy*C+x]||S[y*C+cx]))continue;
   if(blockedFeet((x+.5)*T,(y+.5)*T)||!lineClear((cx+.5)*T,(cy+.5)*T,(x+.5)*T,(y+.5)*T))continue;
   prev[k]=cur;queue[tail++]=k;
  }
 }
 if(!found)return null;const path=[];for(let k=goal;k!==-1;k=prev[k])path.push([(k%C+.5)*T,(Math.floor(k/C)+.5)*T]);path.reverse();return path;
}
function steerPoint(u,x,y){
 if(!W.solid||lineClear(u.x,u.y,x,y)){u._pp=null;return[x,y]}
 const sx=clamp(Math.floor(u.x/T),0,W.cols-1),sy=clamp(Math.floor(u.y/T),0,W.rows-1),[gx,gy]=nearestFree(Math.floor(x/T),Math.floor(y/T));let p=u._pp;
 if(!p||p.solid!==W.solid||p.gx!==gx||p.gy!==gy||clock-p.t>1.2){p=u._pp={gx,gy,t:clock,solid:W.solid,path:bfsPath(...nearestFree(sx,sy),gx,gy)||[],i:0}}
 while(p.i<p.path.length&&Math.hypot(p.path[p.i][0]-u.x,p.path[p.i][1]-u.y)<1.5)p.i++;
 // Skip to a later waypoint only when the complete foot footprint can get there.
 while(p.i+1<p.path.length&&lineClear(u.x,u.y,...p.path[p.i+1]))p.i++;
 const point=p.path[p.i];return point&&lineClear(u.x,u.y,...point)?point:[u.x,u.y];
}

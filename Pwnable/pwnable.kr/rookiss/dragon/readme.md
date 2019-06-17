---
layout : post 
title : Dragonnnn
subtitle : Rookiss Pwnable.kr 
image : /Pwnable/pwnable.kr/rookiss/dragon/dragon.png 
--- 

# Mở đầu  
Bài này chỉ cần có ý tưởng là làm ra được. Ý tưởng là overflow int . Lúc đầu mình không có ý tưởng nên không phát hiện ra được lỗi gì cả 😭😭😭 
Fail vl . Thế nên mình làm luôn một cái check list để lưu lại ý tưởng để sau này bí còn cái mà tìm. 

# Phân tích binary  

**hàm FightDragon** 
```c
void __cdecl FightDragon(int choice)
{
  char time; // al
  void *name; // ST1C_4
  int res; // [esp+10h] [ebp-18h]
  _DWORD *player; // [esp+14h] [ebp-14h]
  _DWORD *monster; // [esp+18h] [ebp-10h]

  player = malloc(0x10u);
  monster = malloc(0x10u);
  time = Count++;
  if ( time & 1 )
  {
    monster[1] = 1;
    *((_BYTE *)monster + 8) = 80;               // HP
    *((_BYTE *)monster + 9) = 4;                // Life Regeneration
    monster[3] = 10;                            // damage
    *monster = PrintMonsterInfo;
    puts("Mama Dragon Has Appeared!");
  }
  else
  {
    monster[1] = 0;
    *((_BYTE *)monster + 8) = 50;               // HP
    *((_BYTE *)monster + 9) = 5;                // Life Regeneration
    monster[3] = 30;                            // damage 
    *monster = PrintMonsterInfo;
    puts("Baby Dragon Has Appeared!");
  }
  if ( choice == 1 )
  {
    *player = 1;
    player[1] = 42;                             // HP
    player[2] = 50;                             // MP
    player[3] = PrintPlayerInfo;
    res = PriestAttack((int)player, monster);
  }
  else
  {
    if ( choice != 2 )
      return;
    *player = 2;
    player[1] = 50;                             // HP
    player[2] = 0;                              // MP
    player[3] = PrintPlayerInfo;
    res = KnightAttack((int)player, monster);
  }
  if ( res )
  {
    puts("Well Done Hero! You Killed The Dragon!");
    puts("The World Will Remember You As:");
    name = malloc(0x10u);
    __isoc99_scanf("%16s", name);
    puts("And The Dragon You Have Defeated Was Called:");
    ((void (__cdecl *)(_DWORD *))*monster)(monster);
  }
  else
  {
    puts("\nYou Have Been Defeated!");
  }
  free(player);
}
```  

**Hàm PriestAttack ** 
```c
int __cdecl PriestAttack(int player, void *monster)
{
  int choice; // eax

  do
  {
    (*(void (__cdecl **)(void *))monster)(monster);
    (*(void (__cdecl **)(int))(player + 12))(player);
    choice = GetChoice();
    switch ( choice )
    {
      case 2:                                   // h?i mana nhung b? con r?ng t?n công , d?ng th?i con r?ng h?i máu
        puts("Clarity! Your Mana Has Been Refreshed");
        *(_DWORD *)(player + 8) = 50;
        printf("But The Dragon Deals %d Damage To You!\n", *((_DWORD *)monster + 3));
        *(_DWORD *)(player + 4) -= *((_DWORD *)monster + 3);
        printf("And The Dragon Heals %d HP!\n", *((char *)monster + 9));
        *((_BYTE *)monster + 8) += *((_BYTE *)monster + 9);
        break;
      case 3:                                   // Không b? r?ng t?n công nhung t?n 25 MP , r?ng h?i máu
        if ( *(_DWORD *)(player + 8) <= 24 )
        {
          puts("Not Enough MP!");
        }
        else
        {
          puts("HolyShield! You Are Temporarily Invincible...");
          printf("But The Dragon Heals %d HP!\n", *((char *)monster + 9));
          *((_BYTE *)monster + 8) += *((_BYTE *)monster + 9);
          *(_DWORD *)(player + 8) -= 25;
        }
        break;
      case 1:                                   // t?n công r?ng gây 20 damage t?n 10 MP, r?ng t?n công l?i mình m?t máu
        if ( *(_DWORD *)(player + 8) <= 9 )
        {
          puts("Not Enough MP!");
        }
        else
        {
          printf("Holy Bolt Deals %d Damage To The Dragon!\n", 20);
          *((_BYTE *)monster + 8) -= 20;
          *(_DWORD *)(player + 8) -= 10;
          printf("But The Dragon Deals %d Damage To You!\n", *((_DWORD *)monster + 3));
          *(_DWORD *)(player + 4) -= *((_DWORD *)monster + 3);
          printf("And The Dragon Heals %d HP!\n", *((char *)monster + 9));
          *((_BYTE *)monster + 8) += *((_BYTE *)monster + 9);
        }
        break;
    }
    if ( *(_DWORD *)(player + 4) <= 0 )
    {
      free(monster);
      return 0;
    }
  }
  while ( *((_BYTE *)monster + 8) > 0 );
  free(monster);
  return 1;
}
``` 

Theo ý tưởng trên thì chúng ta sẽ dùng hàm **PriestAttack** để tấn công con rồng mẹ . Rồng mẹ có 80 HP , nên ta sẽ cố tràn quá 128 HP , vì HP 
được lưu trong BYTE nên tràn quá 128 HP thì máu sẽ thành âm. Có ý tưởng trên thì mọi chuyện ez vãi chưởng . 
Việc còn lại mình để các bạn . 

# Kết  
 👇 👇 👇 Mai lại try hard thêm nữa . Minnig vẫn chưa đủ .  

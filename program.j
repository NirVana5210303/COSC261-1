.class public Program
.super java/lang/Object
.method public <init>()V
aload_0
invokenonvirtual java/lang/Object/<init>()V
return
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 4
.limit stack 1024
new java/util/Scanner
dup
getstatic java/lang/System.in Ljava/io/InputStream;
invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V
astore 0
iload 1
sipush 50
if_icmplt l3
iload 2
sipush 1000
if_icmpgt l1
l3:
sipush 1
istore 3
goto l2
l1:
sipush 2
istore 3
l2:
return
.end method


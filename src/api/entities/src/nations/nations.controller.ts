import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { NationsService } from './nations.service';
import { Prisma } from '@prisma/client';

@Controller('nations')
export class NationsController {
  constructor(private readonly nationsService: NationsService) {}

  @Post()
  create(@Body() createNationDto: Prisma.nationCreateInput) {
    return this.nationsService.create(createNationDto);
  }

  @Get()
  findAll() {
    return this.nationsService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.nationsService.findOne(id as string);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateNationDto: Prisma.nationUpdateInput) {
    return this.nationsService.update(id as string, updateNationDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.nationsService.remove(id as string);
  }
}
